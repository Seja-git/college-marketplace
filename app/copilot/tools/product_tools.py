from app.models import Item
from app import db

from ai_features.utils.semantic_search import search as semantic_search


def search_products(
    query: str,
    category: str = "",
    min_price: float = 0,
    max_price: float = 0
) -> list:
    """
    Search currently available marketplace products.

    Use this when the user wants to find products, listings,
    items, or products matching a description.

    Args:
        query: What the user is looking for.
        category: Optional marketplace category.
        min_price: Optional minimum price.
        max_price: Optional maximum price.

    Returns:
        A list of currently available marketplace listings.
    """

    results = semantic_search(
        query,
        top_n=50
    )


    if results.empty:
        return []


    ids = results["id"].tolist()


    query_obj = Item.query.filter(
        Item.id.in_(ids),
        Item.is_sold == False
    )


    if category:
        query_obj = query_obj.filter(
            Item.category.ilike(
                f"%{category}%"
            )
        )


    if min_price > 0:
        query_obj = query_obj.filter(
            Item.price >= min_price
        )


    if max_price > 0:
        query_obj = query_obj.filter(
            Item.price <= max_price
        )


    items = query_obj.all()


    item_map = {
        item.id: item
        for item in items
    }


    output = []


    for item_id in ids:

        item = item_map.get(item_id)

        if not item:
            continue


        output.append({
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "price": item.price,
            "category": item.category,
            "seller_id": item.user_id,
            "is_sold": item.is_sold
        })


        if len(output) >= 10:
            break


    return output


def get_product_details(item_id: int) -> dict:
    """
    Get detailed information about one marketplace product.

    Use this when the user asks about a specific listing.

    Args:
        item_id: The marketplace item ID.

    Returns:
        Product information.
    """

    item = Item.query.get(item_id)


    if not item:

        return {
            "found": False,
            "message": "Product not found."
        }


    return {
        "found": True,
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "price": item.price,
        "category": item.category,
        "seller_id": item.user_id,
        "is_sold": item.is_sold,
        "created_at": (
            item.created_at.isoformat()
            if item.created_at
            else None
        )
    }