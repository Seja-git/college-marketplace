from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ------------------------------------------------
# Paths
# ------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

KNOWLEDGE_DIR = BASE_DIR / "knowledge"


# ------------------------------------------------
# Storage
# ------------------------------------------------

documents = []

vectorizer = None
document_vectors = None


# ------------------------------------------------
# Load knowledge documents
# ------------------------------------------------

def load_knowledge_base():

    global documents

    if documents:
        return

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            continue

        documents.append({
            "source": file_path.name,
            "content": text
        })


# ------------------------------------------------
# Build TF-IDF index
# ------------------------------------------------

def build_index():

    global vectorizer
    global document_vectors

    load_knowledge_base()

    if not documents:
        raise ValueError(
            "No knowledge documents found."
        )

    texts = [
        document["content"]
        for document in documents
    ]

    vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    sublinear_tf=True
    )

    document_vectors = vectorizer.fit_transform(
        texts
    )


# ------------------------------------------------
# Retrieve relevant knowledge
# ------------------------------------------------

def retrieve_knowledge(
    query: str,
    top_k: int = 3
):

    if not query:
        return []

    if vectorizer is None:
        build_index()

    query_vector = vectorizer.transform(
        [query]
    )

    similarity_scores = cosine_similarity(
        query_vector,
        document_vectors
    ).flatten()

    ranked_indices = (
        similarity_scores
        .argsort()[::-1]
    )

    results = []

    for index in ranked_indices:

        score = similarity_scores[index]

        if score <= 0:
            continue

        document = documents[index]

        results.append({
            "source": document["source"],
            "content": document["content"],
            "score": round(
                float(score),
                3
            )
        })

        if len(results) >= top_k:
            break

    return results


# ------------------------------------------------
# Create context for Gemini
# ------------------------------------------------

def get_rag_context(
    query: str,
    top_k: int = 3
):

    results = retrieve_knowledge(
        query,
        top_k
    )

    if not results:
        return ""

    context_parts = []

    for result in results:

        context_parts.append(
            f"""
SOURCE: {result['source']}

{result['content']}
"""
        )

    return (
        "\n\n"
        "RETRIEVED MARKETPLACE KNOWLEDGE:\n"
        + "\n".join(context_parts)
    )