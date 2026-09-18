from app.models import Item

from ai_features.utils.semantic_search import search as semantic_search


def compare_product_prices(
    query: str
) -> dict:
    """
    Compare prices of currently available marketplace
    listings matching a product query.

    Use this when the user wants to compare prices or
    understand the current price range.

    Args:
        query: Product description or product name.

    Returns:
        Price comparison information.
    """

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
            "price": item.price,
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