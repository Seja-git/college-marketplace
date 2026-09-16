from google import genai
from google.genai import types

from dotenv import load_dotenv
import os

from app.copilot.prompts import SYSTEM_PROMPT


# Load environment variables
load_dotenv()


# Get Gemini API key
API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file"
    )


# Initialize Gemini client
client = genai.Client(
    api_key=API_KEY
)


# Gemini model
MODEL_NAME = "gemini-3.5-flash"


def get_copilot_response(user_message):
    """
    Generate a response from the AI Marketplace Copilot.
    """

    if not user_message:
        return "Please enter a message."

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )

    return response.text.strip()