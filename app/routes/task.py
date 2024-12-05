from flask import Blueprint, jsonify, request

from app.common.exceptions import ValidationError
from app.controllers.task import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    delete_task,
    generate_task,
    assign_existing_task,
    complete_task
)

task_bp = Blueprint("tasks", __name__)

@task_bp.route("/", methods=["POST"])
def create_task_route():
    data = request.get_json()

    if not data or not isinstance(data, dict):
        raise ValidationError("Invalid request body. Expected a JSON object.")

    required_fields = ['description', 'category']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
    
    request_data = {}
    request_data["description"] = data.get("description")
    request_data["category_name"] = data.get("category")

    result = create_task(request_data)
    return jsonify(result), 201

@task_bp.route("/", methods=["GET"])
def get_all_tasks_route():
    result = get_all_tasks()
    return jsonify(result), 200

@task_bp.route("/<int:id>", methods=["GET"])
def get_task_by_id_route(id):
    result = get_task_by_id(id)
    return jsonify(result), 200

@task_bp.route("/<int:id>", methods=["PUT"])
def update_task_route(id):
    data = request.get_json()

    if not data or not isinstance(data, dict):
        raise ValidationError("Invalid request body. Expected a JSON object.")

    request_data = {}
    if "description" in data:
        request_data["description"] = data.get("description")
    if "category" in data:
        request_data["category_name"] = data.get("category")

    result = update_task(id, request_data)
    return jsonify(result), 200

@task_bp.route("/<int:id>", methods=["DELETE"])
def delete_task_route(id):
    result = delete_task(id)
    return jsonify(result), 204

@task_bp.route("/generate", methods=["POST"])
def generate_task_route():
    data = request.get_json()

    if not data or not isinstance(data, dict):
        raise ValidationError("Invalid request body. Expected a JSON object.")

    required_fields = ["telegram_id"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
    
    request_data = {}
    request_data["telegram_id"] = data.get("telegram_id")
    request_data["category_name"] = data.get("category", "")

    result = generate_task(request_data)
    return jsonify(result), 200

@task_bp.route("/get", methods=["POST"])
def assign_existing_task_route():
    data = request.get_json()

    if not data or not isinstance(data, dict):
        raise ValidationError("Invalid request body. Expected a JSON object.")

    required_fields = ["telegram_id"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
    
    request_data = {}
    request_data["telegram_id"] = data.get("telegram_id")
    request_data["category_name"] = data.get("category", "")

    result = assign_existing_task(request_data)
    return jsonify(result), 200

@task_bp.route("/<int:id>/complete", methods=["POST"])
def complete_task_route(id):
    data = request.get_json()

    if not data or not isinstance(data, dict):
        raise ValidationError("Invalid request body. Expected a JSON object.")

    required_fields = ["telegram_id"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

    request_data = {}
    request_data["telegram_id"] = data.get("telegram_id")

    result = complete_task(id, request_data)
    return jsonify(result), 200