from sqlalchemy.orm import joinedload
from sqlalchemy import func
from openai import OpenAIError

from app.models.task import Task
from app.models.category import Category
from app.models.user import User
from app.models.user_task import UserTask
from app.common.db import db
from app.common.openai import openai_client

def create_task(data):
    description = data.get("description")
    category_name = data.get("category_name")

    category = Category.query.filter_by(name=category_name).first()
    if not category:
        raise ValueError("Category not found")

    task = Task(
        description = description,
        category_id = category.id,
    )
    db.session.add(task)
    db.session.commit()
    return task

def get_all_tasks():
    return Task.query.options(joinedload(Task.category)).all()

def get_task_by_id(id):
    return Task.query.options(joinedload(Task.category)).get(id)

def update_task(id, data):
    description = data.get("description")
    category_name = data.get("category_name")

    task = Task.query.get(id)
    if task:
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            raise ValueError("Category not found")

        task.description = description
        task.category_id = category.id
        db.session.commit()
        return task
    return None

def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return task
    return None

def generate_task(data):
    telegram_id = data.get("telegram_id")
    category_name = data.get("category_name")

    user = User.query.filter_by(telegram_id=telegram_id).first()
    if not user:
        raise ValueError(f"User not found")   

    if not category_name:
        category = Category.query.order_by(func.random()).first()
        if not category:
            raise ValueError("Category not found")
        category_name = category.name
    
    messages = [
        {
            "role": "system",
            "content":  f"Generate a random, short task that is 10-15 words long. "
                        f"Example: 'Write a letter to your future self',"
                        f"'Cook a dish with only ingredients you already have at home' or"
                        f"'Take a photo of something blue and share it'."
        },
        {
            "role": "user",
            "content": f"Generate a random task. Make it related to the category: {category_name}."
        }
    ]

    try:
        chat_completion = openai_client.chat.completions.create(
            messages = messages,
            model = "gpt-4o-mini",
            temperature=2,
            max_tokens=50,
        )   
        description = chat_completion.choices[0].message.content.strip()

        task = create_task({
            "description": description,
            "category_name": category_name,
        })

        assign_task_to_user(task, user)

        return task
    
    except OpenAIError as e:
        raise ValueError(f"Failed to generate task: {str(e)}")

def assign_task_to_user(task, user):
    user_task = UserTask(
        user_id = user.id,
        task_id = task.id,
    )
    db.session.add(user_task)
    db.session.commit()
    return user_task

def get_existing_task(data):
    telegram_id = data.get("telegram_id")
    category_name = data.get("category_name")

    user = User.query.filter_by(telegram_id=telegram_id).first()
    if not user:
        raise ValueError(f"User not found")   

    if not category_name:
        category = Category.query.order_by(func.random()).first()
    else:
        category = Category.query.filter_by(name=category_name).first()
    
    if not category:
        raise ValueError("Category not found")

    task = Task.query.filter_by(category_id=category.id).order_by(func.random()).first()
    if not task:
        raise ValueError("Task not found")

    assign_task_to_user(task, user)

    return task
    