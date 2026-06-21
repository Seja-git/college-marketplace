

from flask import Flask, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


app = Flask(__name__)


app.config["SECRET_KEY"] = "my_super_secret_key_123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"

db = SQLAlchemy(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# -------------------
# User Model
# -------------------
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


# -------------------
# Item Model
# -------------------
class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))

    description = db.Column(db.Text)

    price = db.Column(db.Float)

    category = db.Column(db.String(50))


# -------------------
# Flask Login User Loader
# -------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -------------------
# Create Tables
# -------------------
with app.app_context():
    db.create_all()


# -------------------
# Home
# -------------------
@app.route("/")
def home():
    return """
    <h1>College Marketplace</h1>

    <a href='/items'>View Items</a><br>
    <a href='/register'>Register</a><br>
    <a href='/login'>Login</a><br>
    <a href='/logout'>Logout</a>
    """




# -------------------
# Register
# -------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect("/items")

        return "Invalid Email or Password"

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/")


# -------------------
# View All Items
# -------------------
@app.route("/items")
def items():

    all_items = Item.query.all()

    return render_template(
        "items.html",
        items=all_items
    )


# -------------------
# Item Detail
# -------------------
@app.route("/item/<int:item_id>")
def item_detail(item_id):

    item = Item.query.get_or_404(item_id)

    return render_template(
        "item_detail.html",
        item=item
    )


# -------------------
# Create Item
# -------------------
@app.route("/create", methods=["GET", "POST"])
@login_required
def create_item():

    

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        price = request.form["price"]
        category = request.form["category"]

        item = Item(
            title=title,
            description=description,
            price=price,
            category=category
        )

        db.session.add(item)
        db.session.commit()

        return redirect("/items")

    return render_template("add_item.html")


# -------------------
# Edit Item
# -------------------
@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):

    item = Item.query.get_or_404(item_id)

    if request.method == "POST":

        item.title = request.form["title"]
        item.description = request.form["description"]
        item.price = request.form["price"]
        item.category = request.form["category"]

        db.session.commit()

        return redirect(f"/item/{item.id}")

    return render_template(
        "edit_item.html",
        item=item
    )


# -------------------
# Delete Item
# -------------------
@app.route("/delete/<int:item_id>")
def delete_item(item_id):

    item = Item.query.get_or_404(item_id)

    db.session.delete(item)

    db.session.commit()

    return redirect("/items")

@app.route("/profile")
@login_required
def profile():
    return f"Welcome {current_user.username}"


if __name__ == "__main__":
    app.run(debug=True)