from sqlalchemy.exc import SQLAlchemyError

from app.models.category import Category
from app.common.db import db
from app.common.exceptions import DatabaseError, NotFoundError

def create_category(data):
    try:
        name = data.get("name")
        category = Category(
            name = name,
        )
        db.session.add(category)
        db.session.commit()
        result = {
            "id": category.id,
            "name": category.name,
        }
        return result
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def get_all_categories():
    try:
        categories = Category.query.all()
        result = [{"id": category.id, "name": category.name} for category in categories]
        return result
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def get_category_by_id(id):
    try:
        category = Category.query.get(id)
        if not category:
            raise NotFoundError("Category not found.")
        
        result = {
            "id": category.id,
            "name": category.name
        }
        return result
    except NotFoundError as e:
        raise NotFoundError(f"{str(e)}")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def update_category(id, data):
    try:
        category = Category.query.get(id)
        if not category:
            raise NotFoundError("Category not found.")
        
        if "name" in data:
            category.name = data.get("name")

        db.session.commit()
        result = {
            "id": category.id,
            "name": category.name,
        }        
        return result
    except NotFoundError as e:
        raise NotFoundError(f"{str(e)}")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def delete_category(id):
    try:
        category = Category.query.get(id)
        if not category:
            raise NotFoundError("Category not found.")
        
        db.session.delete(category)
        db.session.commit()
        result = {"message": "Category deleted successfully"}
        return result
    except NotFoundError as e:
        raise NotFoundError(f"{str(e)}")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")