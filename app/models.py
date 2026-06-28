from flask_login import UserMixin

from app import db, login_manager


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    college = db.Column(
        db.String(100),
        nullable=False
    )

    items = db.relationship(
        "Item",
        backref="owner",
        lazy=True
    )


class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))

    description = db.Column(db.Text)

    price = db.Column(db.Float)

    category = db.Column(db.String(50))

    image = db.Column(db.String(255), nullable=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))