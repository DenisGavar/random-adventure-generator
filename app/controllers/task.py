from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from openai import OpenAIError
from datetime import datetime

from app.models.task import Task
from app.models.category import Category
from app.models.user import User
from app.models.user_task import UserTask
from app.common.db import db
from app.common.openai import openai_client
from app.common.exceptions import DatabaseError, NotFoundError, AIGenerationError

CONTENT = """You are a task generator. Generate a random, short task that is 10-15 words long.
Your tasks should be clear, concise, and meaningful.
Each task should be related to the category provided.
Example: 'Write a letter to your future self',
'Cook a dish with only ingredients you already have at home' or
'Take a photo of something blue and share it'.
"""

def create_task(data):
    try:
        description = data.get("description")
        category_name = data.get("category_name")

        category = Category.query.filter_by(name=category_name).first()
        if not category:
            raise NotFoundError("Category not found.")

        task = Task(
            description = description,
            category_id = category.id,
        )
        db.session.add(task)
        db.session.commit()

        result = {
            "id": task.id,
            "description": task.description,
            "category": category_name,
        }
        return result
    except NotFoundError as e:
        raise NotFoundError(f"{str(e)}")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def get_all_tasks():
    try:
        tasks = Task.query.options(joinedload(Task.category)).all()
        result = [
            {
                "id": task.id,
                "description": task.description,
                "category": task.category.name,
            }
            for task in tasks
        ]

        return result
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def get_task_by_id(id):
    try:
        task = Task.query.options(joinedload(Task.category)).get(id)
        if not task:
            raise NotFoundError("Task not found.")
        
        result = {
            "id": task.id,
            "description": task.description,
            "category": task.category.name,
        }
        return result
    except NotFoundError as e:
        raise NotFoundError(f"{str(e)}")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def update_task(id, data):
    try:
        task = Task.query.get(id)
        if not task:
            raise NotFoundError("Task not found.")
        
        if "description" in data:
            task.description = data.get("description")
        if "category_name" in data:
            category_name = data.get("category_name")
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                raise NotFoundError("Category not found")
            task.category_id = category.id

        db.session.commit()
        result = {
            "id": task.id,
            "description": task.description,
            "category": task.category.name,
        }        
        return result
    except NotFoundError as e:
        raise NotFoundError(f"{str(e)}")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def delete_task(id):
    try:
        task = Task.query.get(id)
        if not task:
            raise NotFoundError("Task not found.")
        
        db.session.delete(task)
        db.session.commit()
        result = {"message": "Task deleted successfully"}
        return result
    except NotFoundError as e:
        raise NotFoundError(f"{str(e)}")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def assign_task_to_user(task_id, user_id):
    user_task = UserTask(
        user_id = user_id,
        task_id = task_id,
    )
    db.session.add(user_task)
    db.session.commit()

def generate_task(data):
    try:
        telegram_id = data.get("telegram_id")
        category_name = data.get("category_name")

        user = User.query.filter_by(telegram_id=telegram_id).first()
        if not user:
            raise NotFoundError("User not found")          

        if not category_name:
            category = Category.query.order_by(func.random()).first()
            if not category:
                raise NotFoundError("Category not found")
            category_name = category.name

        messages = [
            {
                "role": "system",
                "content":  CONTENT,
            },
            {
                "role": "user",
                "content": f"Generate a random task. Make it related to the category: {category_name}."
            }
        ]
        chat_completion = openai_client.chat.completions.create(
            messages = messages,
            model = "gpt-4o-mini",
            temperature=1,
            max_tokens=50,
        )   
        description = chat_completion.choices[0].message.content.strip()

        task = create_task({
            "description": description,
            "category_name": category_name,
        })

        assign_task_to_user(task["id"], user.id)
     
        return task

    except NotFoundError as e:
        raise NotFoundError(f"{str(e)}")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except OpenAIError as e:
        raise AIGenerationError(f"Failed to generate task: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")

def assign_existing_task(data):
    try:
        telegram_id = data.get("telegram_id")
        category_name = data.get("category_name")

        user = User.query.filter_by(telegram_id=telegram_id).first()
        if not user:
            raise NotFoundError("User not found")   

        if not category_name:
            category = Category.query.order_by(func.random()).first()
        else:
            category = Category.query.filter_by(name=category_name).first()
        
        if not category:
            raise NotFoundError("Category not found")

        task = Task.query.filter_by(category_id=category.id).order_by(func.random()).first()
        if not task:
            raise NotFoundError("Task not found")

        assign_task_to_user(task.id, user.id)

        result = {
            "id": task.id,
            "description": task.description,
            "category": category.name,
        }        
        return result

    except NotFoundError as e:
        raise NotFoundError(f"{str(e)}")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")
    
def complete_task(id, request_data):
    try:
        telegram_id = request_data.get("telegram_id")

        user = User.query.filter_by(telegram_id=telegram_id).first()
        if not user:
            raise NotFoundError("User not found") 
        
        user_task = UserTask.query.filter_by(task_id=id, user_id=user.id).first()
        if not user_task:
            raise NotFoundError("User task not found") 
        
        user_task.status = "completed"
        user_task.completed_at = datetime.now()
        db.session.commit()
        
        result = {"message": "Task completed successfully"}
        return result
    
    except NotFoundError as e:
        raise NotFoundError(f"{str(e)}")
    except SQLAlchemyError as e:
        raise DatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error occurred: {str(e)}")