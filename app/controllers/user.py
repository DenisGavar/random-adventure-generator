from sqlalchemy.exc import SQLAlchemyError

from app.models.user import User
from app.models.task import Task
from app.models.user_task import UserTask
from app.models.category import Category
from app.common.db import db
from app.common.exceptions import DatabaseError, NotFoundError

def create_user(data):
    try:
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
        result = {
            "id": user.id,
            "telegram_id": user.telegram_id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return result
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def get_all_users():
    try:
        users = User.query.all()
        result = [
            {
                "id": user.id,
                "telegram_id": user.telegram_id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
            for user in users
        ]

        return result
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def get_user_by_id(id):
    try:
        user = User.query.get(id)
        if not user:
            raise NotFoundError("User not found.")
        
        result = {
            "id": user.id,
            "telegram_id": user.telegram_id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return result
    except NotFoundError as e:
        raise NotFoundError(f"{str(e)}")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def update_user(id, data):
    try:
        user = User.query.get(id)
        if not user:
            raise NotFoundError("User not found.")
        
        if "telegram_id" in data:
            user.telegram_id = data.get("telegram_id")
        if "first_name" in data:
            user.first_name = data.get("first_name")
        if "username" in data:
            user.username = data.get("username")
        if "last_name" in data:
            user.last_name = data.get("last_name")

        db.session.commit()
        result = {
            "id": user.id,
            "telegram_id": user.telegram_id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }        
        return result
    except NotFoundError as e:
        raise NotFoundError(f"{str(e)}")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            raise NotFoundError("User not found.")
        
        db.session.delete(user)
        db.session.commit()
        result = {"message": "User deleted successfully"}
        return result
    except NotFoundError as e:
        raise NotFoundError(f"{str(e)}")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def get_user_tasks(request_data):
    try:
        telegram_id = request_data.get("telegram_id")
        status = request_data.get("status")

        user = User.query.filter_by(telegram_id=telegram_id).first()
        if not user:
            raise NotFoundError("User not found.")

        user_tasks_query = (
            db.session.query(Task, UserTask, Category)
            .join(UserTask, Task.id == UserTask.task_id)
            .join(Category, Task.category_id == Category.id)
            .filter(UserTask.user_id == user.id)
        )
        if status:
            user_tasks_query = user_tasks_query.filter(UserTask.status == status)

        user_tasks = user_tasks_query.all()

        result = [
            {
                "task_id": task.id,
                "description": task.description,
                "category_name": category.name,
                "status": user_task.status,
                "assigned_at": user_task.created_at,
                "completed_at": user_task.completed_at,
            }
            for task, user_task, category in user_tasks
        ]
        return result
    except NotFoundError as e:
        raise NotFoundError(f"{str(e)}")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")
