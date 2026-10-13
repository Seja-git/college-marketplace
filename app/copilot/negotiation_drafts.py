

    
import json
import logging
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

logger = logging.getLogger("copilot.negotiation")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)

# Keep consistent with the model configured in your existing agent.
MODEL_NAME = "gemini-3.5-flash"

ALLOWED_ACTIONS = {
    "ask_condition",
    "negotiate_price",
    "draft_offer",
    "draft_counteroffer",
    "clarify_next_steps",
}


def generate_negotiation_draft(
    action,
    item_title,
    listed_price,
    recent_messages,
    price_comparison=None,
):
    if action not in ALLOWED_ACTIONS:
        raise ValueError("Unsupported draft action.")

    recent_context = []

    for message in recent_messages[-6:]:
        if not isinstance(message, dict):
            continue

        recent_context.append({
            "sender": str(message.get("sender", "participant"))[:30],
            "text": str(message.get("text", ""))[:1000],
        })

    context = {
        "product_title": str(item_title)[:200],
        "listed_price_inr": listed_price,
        "recent_messages": recent_context,
        "comparable_listing_data": price_comparison or {},
        "requested_action": action,
    }

    prompt = f"""
You are a concise assistant for a college second-hand marketplace.

Create one natural, polite message draft for an existing buyer-seller chat.
Use INR (Indian rupees) for prices.

Use only facts present in the supplied context.
Never invent product condition, specifications, seller statements,
comparable prices, or discounts.

If negotiating, treat the listed price as the asking price, not proof
of the product's market value. Use comparable listing data only when
available. Do not invent an offer amount.

The result is a draft only. It must not claim that a message was sent.

Return JSON with exactly these keys:
- draft: the proposed message
- explanation: a brief explanation of the approach

Context:
{json.dumps(context, ensure_ascii=False)}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )

        result = json.loads(response.text or "{}")
        draft = result.get("draft")

        if not isinstance(draft, str) or not draft.strip():
            raise ValueError("Gemini returned an empty draft.")

        return {
            "draft": draft.strip(),
            "explanation": str(result.get("explanation", "")).strip(),
        }

    except Exception:
        logger.exception("Negotiation draft generation failed")
        raise