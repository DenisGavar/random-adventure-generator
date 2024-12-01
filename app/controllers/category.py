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

def get_all_categories():
    return Category.query.all()

def get_category_by_id(id):
    return Category.query.get(id)

def update_category(id, data):
    category = Category.query.get(id)
    if category:
        category.name = data.get("name")
        db.session.commit()
        return category
    return None

def delete_category(id):
    category = Category.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return category
    return None