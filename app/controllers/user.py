from app.models.user import User
from app.common.db import db

def create_user(data):
    telegram_id = data.get("telegram_id")
    username = data.get("username")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    user = User(
        telegram_id = telegram_id,
        username = username,
        first_name = first_name,
        last_name = last_name,
    )
    db.session.add(user)
    db.session.commit()
    return user

def get_all_users():
    return User.query.all()

def get_user_by_id(id):
    return User.query.get(id)

def get_users_by_filter(filters):
    query = User.query
    for field, value in filters.items():
        query = query.filter(getattr(User, field) == value)  
    return query.all()

def update_user(id, data):
    user = User.query.get(id)
    if user:
        if "telegram_id" in data:
            user.telegram_id = data.get("telegram_id")
        if "first_name" in data:
            user.first_name = data.get("first_name")
        if "username" in data:
            user.username = data.get("username")
        if "last_name" in data:
            user.last_name = data.get("last_name")

        db.session.commit()
        return user
    return None

def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return user
    return None