

from google import genai
from google.genai import types

from dotenv import load_dotenv
import os

from flask_login import current_user

from app.copilot.prompts import SYSTEM_PROMPT

from app.copilot.tools.product_tools import (
    search_products,
    get_product_details
)

from app.copilot.tools.price_tools import (
    compare_product_prices
)

from app.copilot.tools.seller_tools import (
    get_seller_information,
    get_seller_reviews
)

from app.copilot.tools.wishlist_tools import (
    add_to_wishlist
)


# ---------------------------------------------------------
# ENVIRONMENT
# ---------------------------------------------------------

load_dotenv()


API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


if not API_KEY:

    raise ValueError(
        "GEMINI_API_KEY not found in .env file"
    )


# ---------------------------------------------------------
# GEMINI CLIENT
# ---------------------------------------------------------

client = genai.Client(
    api_key=API_KEY
)


MODEL_NAME = "gemini-3.5-flash"


# ---------------------------------------------------------
# COPILOT RESPONSE
# ---------------------------------------------------------

def get_copilot_response(user_message):

    if not user_message:

        return "Please enter a message."


    # -----------------------------------------------------
    # USER-SPECIFIC TOOL
    # -----------------------------------------------------

    current_user_id = current_user.id


    def add_current_user_to_wishlist(
        item_id: int
    ) -> dict:
        """
        Add a marketplace item to the currently logged-in
        user's wishlist.

        Args:
            item_id: The marketplace item ID.
        """

        return add_to_wishlist(
            current_user_id,
            item_id
        )


    # -----------------------------------------------------
    # MARKETPLACE TOOLS
    # -----------------------------------------------------

    tools = [

        search_products,

        get_product_details,

        compare_product_prices,

        get_seller_information,

        get_seller_reviews,

        add_current_user_to_wishlist

    ]


    # -----------------------------------------------------
    # GEMINI
    # -----------------------------------------------------

    response = client.models.generate_content(

        model=MODEL_NAME,

        contents=user_message,

        config=types.GenerateContentConfig(

            system_instruction=SYSTEM_PROMPT,

            tools=tools

        )

    )


    return response.text.strip()