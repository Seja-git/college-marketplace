


import pandas as pd
from app import create_app
from app.models import Item

app = create_app()

with app.app_context():
    items = Item.query.all()

    data = []

    for item in items:
        data.append({
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "price": item.price,
            "category": item.category,
            "image": item.image,
            "seller": item.owner.username if item.owner else "",
            "college": item.owner.college if item.owner else "",
            "is_sold": item.is_sold,
            "created_at": item.created_at
        })

df = pd.DataFrame(data)

df.to_csv("marketplace.csv", index=False)

print(f"Exported {len(df)} items successfully!")