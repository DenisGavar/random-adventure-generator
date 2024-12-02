from sqlalchemy.orm import joinedload

from app.models.task import Task
from app.models.category import Category
from app.common.db import db

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