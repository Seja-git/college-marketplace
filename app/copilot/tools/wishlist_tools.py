from app import db
from app.models import Item, Wishlist


def add_to_wishlist(
    user_id: int,
    item_id: int
) -> dict:
    """
    Add an available marketplace item to the current user's wishlist.

    Args:
        user_id: The authenticated user's ID.
        item_id: The marketplace item ID.

    Returns:
        Result of the wishlist operation.
    """

    item = Item.query.get(item_id)


    if not item:

        return {
            "success": False,
            "message": "Item not found."
        }


    if item.is_sold:

        return {
            "success": False,
            "message": "This item has already been sold."
        }


    existing = Wishlist.query.filter_by(
        user_id=user_id,
        item_id=item_id
    ).first()


    if existing:

        return {
            "success": True,
            "message": "Item is already in your wishlist."
        }


    wishlist_item = Wishlist(
        user_id=user_id,
        item_id=item_id
    )


    db.session.add(
        wishlist_item
    )

    db.session.commit()


    return {
        "success": True,
        "message": f"{item.title} was added to your wishlist."
    }