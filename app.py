

from flask import Flask, redirect, request, render_template,flash
import re
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

    username = db.Column(db.String(50), unique=True, nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    college = db.Column(db.String(100), nullable=False)

    items = db.relationship(
        "Item",
        backref="owner",
        lazy=True
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

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )



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
# Register
# -------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        email = request.form["email"].strip()
        college = request.form["college"]
        password = request.form["password"]

        if len(username) < 3:
            flash("Username must be at least 3 characters long", "danger")
            return render_template("register.html")

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(email_pattern, email):
            flash("Please enter a valid email address", "danger")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters long", "danger")
            return render_template("register.html")

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            flash("Username already exists", "danger")
            return render_template("register.html")

        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_email:
            flash("Email already registered", "danger")
            return render_template("register.html")

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            college=college,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip()
        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            flash("Login successful!", "success")

            return redirect("/items")

        flash("Invalid Email or Password", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out.", "success")

    return redirect("/")


# -------------------
# View All Items
# -------------------
@app.route("/items")
@app.route("/")
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
              category=category,
              user_id=current_user.id
              )

        db.session.add(item)
        db.session.commit()

        return redirect("/items")

    return render_template("add_item.html")


# -------------------
# Edit Item
# -------------------
@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_item(item_id):

    item = Item.query.get_or_404(item_id)

    if item.user_id != current_user.id:
        flash("You cannot edit this listing", "danger")
        return redirect("/items")

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
@login_required
def delete_item(item_id):

    item = Item.query.get_or_404(item_id)

    if item.user_id != current_user.id:
        flash("You cannot delete this listing", "danger")
        return redirect("/items")

    db.session.delete(item)

    db.session.commit()

    return redirect("/items")




@app.route("/profile")
@login_required
def profile():

    my_items = Item.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "profile.html",
        items=my_items
    )

if __name__ == "__main__":
    app.run(debug=True)