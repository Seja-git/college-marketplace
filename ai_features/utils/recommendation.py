


from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

df = None
similarity = None
vectorizer = None
id_to_index = None


def load_models():
    global df, similarity, vectorizer, id_to_index

    if df is None:
        df = joblib.load(MODELS_DIR / "dataset.pkl")
        similarity = joblib.load(MODELS_DIR / "similarity.pkl")
        vectorizer = joblib.load(MODELS_DIR / "vectorizer.pkl")

        id_to_index = pd.Series(df.index, index=df["id"])

        print("Recommendation models loaded.")

def recommend(item_id, top_n=5):
    load_models()

    if item_id not in id_to_index:
        return pd.DataFrame()

    item_index = id_to_index[item_id]

    scores = list(enumerate(similarity[item_index]))

    scores = sorted(scores,
                    key=lambda x: x[1],
                    reverse=True)

    recommendations = []

    for idx, score in scores[1:]:

        if not df.iloc[idx]["is_sold"]:

            recommendations.append({
                "id": df.iloc[idx]["id"],
                "title": df.iloc[idx]["title"],
                "price": df.iloc[idx]["price"],
                "category": df.iloc[idx]["category"],
                "similarity": round(score,3)
            })

        if len(recommendations) == top_n:
            break

    return pd.DataFrame(recommendations)