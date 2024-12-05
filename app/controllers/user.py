from app.models.user import User
from app.models.task import Task
from app.models.user_task import UserTask
from app.models.category import Category
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

def get_user_tasks(request_data):
    telegram_id = request_data.get("telegram_id")
    status = request_data.get("status")

    user = User.query.filter_by(telegram_id=telegram_id).first()

    if not user:
        return None, "User not found"

    user_tasks_query = (
        db.session.query(Task, UserTask, Category)
        .join(UserTask, Task.id == UserTask.task_id)
        .join(Category, Task.category_id == Category.id)
        .filter(UserTask.user_id == user.id)
    )

    if status:
        user_tasks_query = user_tasks_query.filter(UserTask.status == status)

    user_tasks = user_tasks_query.all()

    # Format the results
    tasks_data = [
        {
            "id": task.id,
            "description": task.description,
            "category_id": task.category_id,
            "category_name": category.name,
            "status": user_task.status,
            "assigned_at": user_task.created_at,
            "completed_at": user_task.completed_at,
        }
        for task, user_task, category in user_tasks
    ]

    return tasks_data, None
