
from statistics import median

from app.models import Item
from ai_features.utils.semantic_search import search as semantic_search


def compare_product_prices(query: str) -> dict:

    results = semantic_search(
        query,
        top_n=50
    )

    if results.empty:
        return {
            "found": False,
            "message": "No matching products were found."
        }

    ids = results["id"].tolist()

    items = Item.query.filter(
        Item.id.in_(ids),
        Item.is_sold == False
    ).all()

    if not items:
        return {
            "found": False,
            "message": "No available matching products were found."
        }

    item_map = {
        item.id: item
        for item in items
    }

    listings = []

    for item_id in ids:

        item = item_map.get(item_id)

        if not item:
            continue

        listings.append({
            "id": item.id,
            "title": item.title,
            "price": float(item.price),
            "category": item.category
        })

        if len(listings) >= 10:
            break

    if not listings:
        return {
            "found": False,
            "message": "No available matching products were found."
        }

    prices = [
        listing["price"]
        for listing in listings
    ]

    return {
        "found": True,
        "product_query": query,
        "number_of_listings": len(listings),
        "minimum_price": min(prices),
        "maximum_price": max(prices),
        "average_price": round(
            sum(prices) / len(prices),
            2
        ),
        "listings": listings
    }


def get_price_guidance(query: str) -> dict:

    results = semantic_search(
        query,
        top_n=50
    )

    if results.empty:
        return {
            "found": False,
            "message": "No similar marketplace listings were found."
        }

    ids = results["id"].tolist()

    items = Item.query.filter(
        Item.id.in_(ids),
        Item.is_sold == False
    ).all()

    if not items:
        return {
            "found": False,
            "message": "No similar available listings were found."
        }

    item_map = {
        item.id: item
        for item in items
    }

    listings = []

    for item_id in ids:

        item = item_map.get(item_id)

        if not item:
            continue

        listings.append({
            "id": item.id,
            "title": item.title,
            "price": float(item.price),
            "category": item.category
        })

        if len(listings) >= 10:
            break

    if not listings:
        return {
            "found": False,
            "message": "No similar available listings were found."
        }

    prices = [
        listing["price"]
        for listing in listings
    ]

    minimum_price = min(prices)
    maximum_price = max(prices)

    average_price = sum(prices) / len(prices)

    median_price = median(prices)

    suggested_lower = round(
        median_price * 0.90,
        2
    )

    suggested_upper = round(
        median_price * 1.10,
        2
    )

    return {
        "found": True,
        "product_query": query,
        "number_of_listings": len(listings),

        "minimum_price": minimum_price,
        "maximum_price": maximum_price,

        "average_price": round(
            average_price,
            2
        ),

        "median_price": median_price,

        "suggested_range": {
            "lower": suggested_lower,
            "upper": suggested_upper
        },

        "listings": listings
    }