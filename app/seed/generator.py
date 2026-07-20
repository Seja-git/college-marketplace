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




def generate_title(product):

    name = product["name"]
    brand = product.get("brand", "")

    simple = [
        "{brand} {name}",
        "{name}",
    ]

    condition = [
        "{brand} {name} - Like New",
        "{name} (Excellent Condition)",
        "{name} - Good Condition",
        "Well Maintained {name}",
    ]

    selling = [
        "Selling my {name}",
        "{name} for Sale",
        "Used {name}",
    ]

    r = random.random()

    if r < 0.55:
        pattern = random.choice(simple)
    elif r < 0.85:
        pattern = random.choice(condition)
    else:
        pattern = random.choice(selling)

    return pattern.format(
        brand=brand,
        name=name
    ).replace("  ", " ").strip()

SELL_REASONS = [
    "Graduating this semester.",
    "No longer needed.",
    "Upgraded to a newer one.",
    "Cleaning my hostel room.",
    "Shifting to another city.",
    "Course completed.",
    "Bought a new one."
]

DESCRIPTION_ENDINGS = [
    "Works perfectly and has been maintained well.",
    "Everything is in good working condition.",
    "Still in good condition with regular use.",
    "Suitable for students looking for an affordable option.",
    "A good choice for everyday college use.",
    "Can be used immediately without any issues."
]


def generate_description(product, category, condition):

    description = random.choice(DESCRIPTION_MAP[category])

    brand = product.get("brand", "")
    reason = random.choice(SELL_REASONS)
    ending = random.choice(DESCRIPTION_ENDINGS)

    intro_templates = [

        f"Selling my {brand} {product['name']} as it is no longer needed.",

        f"This {product['name']} is in {condition.lower()} condition and has been used carefully.",

        f"I am selling this {product['name']} after completing my coursework.",

        f"Used this {product['name']} for college and it is still in {condition.lower()} condition.",

        f"Selling this {product['name']} since I have upgraded."
    ]

    intro = random.choice(intro_templates)

    return (
        f"{intro} "
        f"{description} "
        f"{ending} "
        f"Reason for selling: {reason}"
    )