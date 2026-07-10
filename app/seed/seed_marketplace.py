

from .data.books import BOOKS
from .data.notes import NOTES
from .data.electronics import ELECTRONICS
from .data.furniture import FURNITURE
from .data.hostel import HOSTEL
from .data.sports import SPORTS
from .data.cycle import CYCLES
from .data.stationarytools import STATIONERY_TOOLS
from .data.others import OTHERS


import random
from datetime import datetime, timedelta

from app import create_app, db
app = create_app()
from app.models import User, Item, Wishlist, Conversation, Message, Review

from .generator import generate_title, generate_description
from .utils import choose_condition, generate_price

# import your product datasets here
# BOOKS
# ELECTRONICS
# NOTES
# ...

# --------------------------------------------------
# BUILD MASTER PRODUCT LIST
# --------------------------------------------------

ALL_PRODUCTS = []

datasets = [
    ("Books", BOOKS),
    ("Notes", NOTES),
    ("Electronics", ELECTRONICS),
    ("Furniture", FURNITURE),
    ("Hostel Essentials", HOSTEL),
    ("Sports", SPORTS),
    ("Cycles", CYCLES),
    ("Stationery and Tools", STATIONERY_TOOLS),
    ("Others", OTHERS),
]

for category, products in datasets:

    for p in products:

        temp = p.copy()
        temp["category"] = category
        ALL_PRODUCTS.append(temp)

# --------------------------------------------------

CHAT_TEMPLATES = [

    [
        "Hi, is this available?",
        "Yes.",
        "Can you reduce the price?",
        "Sure, a little.",
        "Great. I'll buy it."
    ],

    [
        "Interested.",
        "Available.",
        "Can I collect tomorrow?",
        "Yes."
    ],

    [
        "Still available?",
        "Yes.",
        "Original bill?",
        "Yes, available."
    ]
]

REVIEWS = [

    "Great seller.",
    "Exactly as described.",
    "Very cooperative.",
    "Fast response.",
    "Highly recommended.",
    "Worth the price.",
    "Good experience."
]

# --------------------------------------------------

with app.app_context():

    users = User.query.all()

    if len(users) < 2:

        print("Need at least two users.")
        exit()

    generated_items = []

    # ------------------------------------------
    # Listings
    # ------------------------------------------

    for i in range(500):

        product = random.choice(ALL_PRODUCTS)

        seller = random.choice(users)

        category = product["category"]

        condition = choose_condition()

        item = Item(

            title=generate_title(product),

            description=generate_description(
                product,
                category,
                condition
            ),

            price = generate_price(
              product["price_range"],
               condition
            ),

            category=category,

            image="default.jpg",

            owner=seller,

            created_at=datetime.utcnow()
            - timedelta(
                days=random.randint(0,180),
                hours=random.randint(0,23),
                minutes=random.randint(0,59)
            )

        )

        db.session.add(item)

        generated_items.append(item)

    db.session.commit()

    print("Listings Generated")

    # ------------------------------------------
    # Wishlists
    # ------------------------------------------

    for user in users:

        choices = random.sample(
            generated_items,
            min(5, len(generated_items))
        )

        for item in choices:

            if item.user_id == user.id:
                continue

            db.session.add(

                Wishlist(

                    user_id=user.id,

                    item_id=item.id

                )

            )

    db.session.commit()

    print("Wishlists Generated")

    # ------------------------------------------
    # Conversations
    # ------------------------------------------

    conversations = []

    for i in range(80):

        item = random.choice(generated_items)

        buyers = [u for u in users if u.id != item.user_id]

        if not buyers:
            continue

        buyer = random.choice(buyers)

        convo = Conversation(

            buyer_id=buyer.id,

            seller_id=item.user_id,

            item_id=item.id

        )

        db.session.add(convo)

        conversations.append(convo)

    db.session.commit()

    print("Conversations Generated")

    # ------------------------------------------
    # Messages
    # ------------------------------------------

    for convo in conversations:

        script = random.choice(CHAT_TEMPLATES)

        sender = convo.buyer_id

        for msg in script:

            db.session.add(

                Message(

                    conversation_id=convo.id,

                    sender_id=sender,

                    message=msg,

                    timestamp=datetime.utcnow()
                    - timedelta(
                        days=random.randint(0,30)
                    )

                )

            )

            if sender == convo.buyer_id:
                sender = convo.seller_id
            else:
                sender = convo.buyer_id

    db.session.commit()

    print("Messages Generated")

    # ------------------------------------------
    # Sold Items
    # ------------------------------------------

    sold = random.sample(
        generated_items,
        int(len(generated_items)*0.15)
    )

    for item in sold:

        buyers = [u for u in users if u.id != item.user_id]

        if not buyers:
            continue

        buyer = random.choice(buyers)

        item.is_sold = True

        item.buyer_id = buyer.id

        item.sold_at = datetime.utcnow() - timedelta(
            days=random.randint(1,60)
        )

        db.session.add(

            Review(

                item_id=item.id,

                reviewer_id=buyer.id,

                reviewed_user_id=item.user_id,

                rating=random.randint(4,5),

                comment=random.choice(REVIEWS)

            )

        )

    db.session.commit()

    print("Reviews Generated")

print("Dataset Generation Complete!")