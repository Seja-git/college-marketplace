import random

from .templates import (
    TITLE_PATTERNS,
    BOOK_DESCRIPTIONS,
    NOTES_DESCRIPTIONS,
    ELECTRONICS_DESCRIPTIONS,
    FURNITURE_DESCRIPTIONS,
    HOSTEL_DESCRIPTIONS,
    SPORTS_DESCRIPTIONS,
    CYCLE_DESCRIPTIONS,
    TOOLS_DESCRIPTIONS,
    OTHER_DESCRIPTIONS
)

DESCRIPTION_MAP = {
    "Books": BOOK_DESCRIPTIONS,
    "Notes": NOTES_DESCRIPTIONS,
    "Electronics": ELECTRONICS_DESCRIPTIONS,
    "Furniture": FURNITURE_DESCRIPTIONS,
    "Hostel Essentials": HOSTEL_DESCRIPTIONS,
    "Sports": SPORTS_DESCRIPTIONS,
    "Cycles": CYCLE_DESCRIPTIONS,
    "Stationery and Tools": TOOLS_DESCRIPTIONS,
    "Others": OTHER_DESCRIPTIONS
}

SELL_REASONS = [
    "Graduating this semester.",
    "No longer needed.",
    "Upgraded to a newer one.",
    "Cleaning my hostel room.",
    "Shifting to another city.",
    "Course completed.",
    "Bought a new one."
]


def generate_title(product):
    """
    Generate a realistic listing title.
    """

    pattern = random.choice(TITLE_PATTERNS)

    return pattern.format(
        name=product.get("name", ""),
        brand=product.get("brand", "")
    ).replace("  ", " ").strip()


def generate_description(product, category, condition):
    """
    Generate a realistic marketplace description.
    """

    description = random.choice(DESCRIPTION_MAP[category])

    brand = product.get("brand", "Generic")

    return f"""Brand: {brand}
Condition: {condition}

{description}

Reason for selling:
{random.choice(SELL_REASONS)}

Price slightly negotiable.
""".strip()