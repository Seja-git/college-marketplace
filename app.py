from flask import Flask
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


@app.route("/add")
def add_item():

    item = Item(
        title="Engineering Drawing Kit",
        description="Used for one semester",
        price=200,
        category="Drawing Tools"
    )

    db.session.add(item)
    db.session.commit()

    return "Item Added"

@app.route("/items")
def items():

    all_items = Item.query.all()

    return render_template(
        "items.html",
        items=all_items
    )

if __name__ == "__main__":
    app.run(debug=True)