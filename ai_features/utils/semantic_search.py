
from pathlib import Path
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

# -----------------------------
# Global variables
# -----------------------------
df = None
vectorizer = None
product_vectors = None


# -----------------------------
# Load models only once
# -----------------------------
def load_models():
    global df, vectorizer, product_vectors

    if df is None:
        df = joblib.load(MODELS_DIR / "dataset.pkl")
        vectorizer = joblib.load(MODELS_DIR / "vectorizer.pkl")

        # Convert all products into TF-IDF vectors
        product_vectors = vectorizer.transform(df["combined_text"])

        print("Semantic Search Models Loaded")


# -----------------------------
# Semantic Search
# -----------------------------
def search(query, top_n=10):

    load_models()

    # Convert user query to TF-IDF vector
    query_vector = vectorizer.transform([query.lower()])

    # Compute similarity
    similarity_scores = cosine_similarity(
        query_vector,
        product_vectors
    ).flatten()

    # Highest similarity first
    ranked_indices = similarity_scores.argsort()[::-1]

    results = []

    for idx in ranked_indices:

        # Ignore sold products
        if df.iloc[idx]["is_sold"]:
            continue

        # Ignore completely unrelated products
        if similarity_scores[idx] <= 0.10:
            continue

        results.append({
        "id": df.iloc[idx]["id"],
        "title": df.iloc[idx]["title"],
        "price": df.iloc[idx]["price"],
        "category": df.iloc[idx]["category"],
        "description": df.iloc[idx]["description"],
        "similarity": round(float(similarity_scores[idx]), 3)
        })

        if len(results) == top_n:
            break

    return pd.DataFrame(results)