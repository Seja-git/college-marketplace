

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

from app.copilot.memory import (
    add_user_memory,
    get_user_memories,
    should_store_memory
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

    current_user_id = current_user.id

    # ------------------------------------------------
    # 1. Retrieve long-term memories
    # ------------------------------------------------

    user_memories = get_user_memories(
        current_user_id
    )

    memory_context = ""

    if user_memories:

        memory_context = (
            "\n\nUSER LONG-TERM PREFERENCES:\n"
            + "\n".join(
                f"- {memory}"
                for memory in user_memories
            )
        )

    # ------------------------------------------------
    # 2. Current user's wishlist tool
    # ------------------------------------------------

    def add_current_user_to_wishlist(
        item_id: int
    ) -> dict:

        return add_to_wishlist(
            current_user_id,
            item_id
        )

    # ------------------------------------------------
    # 3. Marketplace tools
    # ------------------------------------------------

    tools = [
        search_products,
        get_product_details,
        compare_product_prices,
        get_seller_information,
        get_seller_reviews,
        add_current_user_to_wishlist
    ]

    # ------------------------------------------------
    # 4. Send memory + current message to Gemini
    # ------------------------------------------------

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=(
            memory_context
            + "\n\nCURRENT USER MESSAGE:\n"
            + user_message
        ),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=tools
        )
    )

    result = response.text.strip()

    # ------------------------------------------------
    # 5. Store useful long-term preference
    # ------------------------------------------------

    if should_store_memory(
        user_message
    ):

        add_user_memory(
            current_user_id,
            user_message
        )

    return result


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