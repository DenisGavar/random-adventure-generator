from flask import Blueprint, jsonify, request
from app.controllers.task import create_task, get_all_tasks, get_task_by_id, update_task, delete_task

task_bp = Blueprint("tasks", __name__)

@task_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    description = data.get("description")
    if not description:
        return jsonify({"error": "Description is required"}), 400
    category_name = data.get("category")
    if not category_name:
        return jsonify({"error": "Category name is required"}), 400

    task = create_task({
        "description": description,
        "category_name": category_name,
    })
    return jsonify({"id": task.id, "description": task.description}), 201

@task_bp.route("/", methods=["GET"])
def get_all():
    tasks = get_all_tasks()
    return jsonify([{
        "id": task.id,
        "description": task.description,
        "category": task.category.name,
    } for task in tasks]), 200

@task_bp.route("/<int:id>", methods=["GET"])
def get_by_id(id):
    task = get_task_by_id(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({
        "id": task.id,
        "description": task.description,
        "category": task.category.name,
    }), 200

@task_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    data = request.get_json()
    description = data.get("description")
    if not description:
        return jsonify({"error": "Description is required"}), 400
    category_name = data.get("category")
    if not category_name:
        return jsonify({"error": "Category name is required"}), 400
        
    task = update_task(id, {
        "description": description,
        "category_name": category_name,
    })
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"id": task.id, "description": task.description}), 200

@task_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    task = delete_task(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted successfully"}), 204