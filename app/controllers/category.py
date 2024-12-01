from app.models.category import Category
from app.common.db import db

def create_category(data):
    name = data.get("name")
    category = Category(
        name = name,
    )
    db.session.add(category)
    db.session.commit()
    return category
