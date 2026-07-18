from google import genai

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")




# Initialize Gemini Client


if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)



def generate_description(
    title,
    category,
    condition,
    price,
    details=""
):
    """
    Generate an AI-powered product description for a college marketplace.
    """

    prompt = f"""
You are an AI assistant for a college second-hand marketplace.

Generate a professional product description. The description should not sound like an advertisement. It should sound genuine and feel like it was written by a college student.

Product Details

Title: {title}

Category: {category}

Condition: {condition}

Price: ₹{price}

Important Details:
{details}

Rules:

- Maximum 70 words.
- Sound like a genuine student listing.
- Mention the condition naturally.
- Include all seller notes.
- Mention who may find the item useful when appropriate.
- Do NOT sound like an advertisement.
- Do NOT begin with "Available for..."
- Do NOT use marketing words like "premium", "best", "grab now", or "high quality".
- Do NOT invent any specifications.
- Return only one paragraph.
- Do not ask the buyer to contact the seller.
- Do not include phrases like "Let me know", "DM me", "Contact me", or "Pick it up".
- End with a natural description of the item instead.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text.strip()