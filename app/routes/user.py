from flask import Blueprint, jsonify, request

from app.common.exceptions import ValidationError
from app.controllers.user import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
    get_user_tasks
)

user_bp = Blueprint("users", __name__)

@user_bp.route("/", methods=["POST"])
def create_user_route():
    data = request.get_json()

    if not data or not isinstance(data, dict):
        raise ValidationError("Invalid request body. Expected a JSON object.")

    required_fields = ['telegram_id', 'first_name']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
    
    request_data = {}
    
    request_data["telegram_id"] = data.get("telegram_id")
    request_data["first_name"] = data.get("first_name")

    request_data["username"] = data.get("username", "")
    request_data["last_name"] = data.get("last_name", "")

    result = create_user(request_data)
    
    return jsonify(result), 201

@user_bp.route("/", methods=["GET"])
def get_all_users_route():
    result = get_all_users()
    return jsonify(result), 200

@user_bp.route("/<int:id>", methods=["GET"])
def get_user_by_id_route(id):
    result = get_user_by_id(id)
    return jsonify(result), 200

@user_bp.route("/<int:id>", methods=["PUT"])
def update_user_route(id):
    data = request.get_json()

    if not data or not isinstance(data, dict):
        raise ValidationError("Invalid request body. Expected a JSON object.")

    request_data = {}

    if "telegram_id" in data:
        request_data["telegram_id"] = data.get("telegram_id")
    if "first_name" in data:
        request_data["first_name"] = data.get("first_name")
    if "username" in data:
        request_data["username"] = data.get("username")
    if "last_name" in data:
        request_data["last_name"] = data.get("last_name")

    result = update_user(id, request_data)
    return jsonify(result), 200

@user_bp.route("/<int:id>", methods=["DELETE"])
def delete_user_route(id):
    result = delete_user(id)
    return jsonify(result), 204

@user_bp.route("/<int:telegram_id>/tasks", methods=["GET"])
def get_user_tasks_route(telegram_id):
    status = request.args.get("status", "")

    request_data = {}
    request_data["telegram_id"] = telegram_id
    request_data["status"] = status

    result = get_user_tasks(request_data)
    return jsonify(result), 200