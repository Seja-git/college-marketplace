from app.models import Review

def get_seller_rating(user_id):
    reviews = Review.query.filter_by(
        reviewed_user_id=user_id
    ).all()

    if not reviews:
        return 0, 0

    avg_rating = round(
        sum(review.rating for review in reviews) / len(reviews),
        1
    )

    return avg_rating, len(reviews)