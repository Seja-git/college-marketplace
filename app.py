from flask import Flask,redirect,request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market.db"

db = SQLAlchemy(app)
class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))

    description = db.Column(db.Text)

    price = db.Column(db.Float)

    category = db.Column(db.String(50))

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return """
    <h1>College Marketplace</h1>

    <a href='/items'>View Items</a>
    """



@app.route("/items")
def items():

    all_items = Item.query.all()

    return render_template(
        "items.html",
        items=all_items
    )

@app.route("/item/<int:item_id>")
def item_detail(item_id):

    item = Item.query.get_or_404(item_id)

    return render_template(
        "item_detail.html",
        item=item
    )



@app.route("/create", methods=["GET", "POST"])
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

@app.route("/delete/<int:item_id>")
def delete_item(item_id):

    item = Item.query.get_or_404(item_id)

    db.session.delete(item)

    db.session.commit()

    return redirect("/items")


if __name__ == "__main__":
    app.run(debug=True)