from app.models import User, Review


def get_seller_information(
    seller_id: int
) -> dict:
    """
    Get seller information and marketplace review summary.

    Use this when the user asks about a seller or wants
    to understand seller ratings.

    Args:
        seller_id: The seller's user ID.

    Returns:
        Seller information and review summary.
    """

    seller = User.query.get(seller_id)


    if not seller:

        return {
            "found": False,
            "message": "Seller not found."
        }


    reviews = Review.query.filter_by(
        reviewed_user_id=seller_id
    ).all()


    ratings = [
        review.rating
        for review in reviews
        if review.rating is not None
    ]


    if ratings:

        average_rating = round(
            sum(ratings) / len(ratings),
            2
        )

    else:

        average_rating = None


    return {
        "found": True,
        "seller_id": seller.id,
        "username": seller.username,
        "college": seller.college,
        "average_rating": average_rating,
        "review_count": len(ratings)
    }


def get_seller_reviews(
    seller_id: int
) -> list:
    """
    Get recent reviews for a marketplace seller.

    Args:
        seller_id: The seller's user ID.

    Returns:
        A list of seller reviews.
    """

    reviews = Review.query.filter_by(
        reviewed_user_id=seller_id
    ).order_by(
        Review.created_at.desc()
    ).limit(10).all()


    output = []


    for review in reviews:

        output.append({
            "rating": review.rating,
            "comment": review.comment,
            "created_at": (
                review.created_at.isoformat()
                if review.created_at
                else None
            )
        })


    return output