import json
import os

from dotenv import load_dotenv
from google import genai

from app.copilot.tools.price_tools import get_price_guidance


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")


client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash"


ALLOWED_CATEGORIES = [
    "Books",
    "Electronics",
    "Notes",
    "Cycles",
    "Furniture",
    "Sports",
    "Hostel Essentials",
    "Stationery",
    "Tools",
    "Others"
]


def generate_listing_assistance(product_info: str) -> dict:

    if not product_info or not product_info.strip():
        return {
            "success": False,
            "message": "Please describe the product you want to sell."
        }

    prompt = f"""
You are helping a student create a second-hand marketplace listing.

The student provided:

{product_info}

Create a listing using ONLY the information provided by the student.

Return ONLY valid JSON in exactly this structure:

{{
    "title": "short product title",
    "description": "clear and honest product description",
    "category": "one category from the allowed categories"
}}

Allowed categories:

{", ".join(ALLOWED_CATEGORIES)}

Rules:

1. Do not invent product specifications.
2. Do not invent condition unless the user mentioned it.
3. Do not invent brand, model, warranty, accessories or features.
4. Keep the title concise.
5. Make the description suitable for a college second-hand marketplace.
6. Do not use exaggerated marketing language.
7. Choose the closest category from the allowed categories.
8. Return JSON only.
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        raw_text = response.text.strip()

        # Remove markdown code fences if Gemini returns them
        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```json", "")
            raw_text = raw_text.replace("```", "")
            raw_text = raw_text.strip()

        listing_data = json.loads(raw_text)

        title = listing_data.get("title", "").strip()
        description = listing_data.get("description", "").strip()
        category = listing_data.get("category", "").strip()

        if not title or not description:
            return {
                "success": False,
                "message": "Could not generate a complete listing."
            }

        if category not in ALLOWED_CATEGORIES:
            category = "Others"

        # -----------------------------------------
        # PRICE GUIDANCE
        # -----------------------------------------

        price_query = f"{title} {category}"

        price_data = get_price_guidance(
            price_query
        )

        return {
            "success": True,
            "title": title,
            "description": description,
            "category": category,
            "price_guidance": price_data
        }

    except json.JSONDecodeError:

        return {
            "success": False,
            "message": "The AI returned an invalid listing format. Please try again."
        }

    except Exception as e:

        print("Listing generation error:", e)

        return {
            "success": False,
            "message": "Unable to generate the listing right now."
        }