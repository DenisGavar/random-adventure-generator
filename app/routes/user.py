from flask import Blueprint, jsonify, request
from app.controllers.user import create_user, get_all_users, get_user_by_id, update_user, delete_user, get_user_tasks

user_bp = Blueprint("users", __name__)

@user_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()

    required_fields = ['telegram_id', 'first_name']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    user_data = {}
    
    user_data["telegram_id"] = data.get("telegram_id")
    user_data["first_name"] = data.get("first_name")

    user_data["username"] = data.get("username", "")
    user_data["last_name"] = data.get("last_name", "")

    user = create_user(user_data)

    user_data = user.__dict__
    user_data.pop('_sa_instance_state', None)
    
    return jsonify(user_data), 201

@user_bp.route("/", methods=["GET"])
def get_all():
    users = get_all_users()

    users_data = [user.__dict__ for user in users]
    
    for user_data in users_data:
        user_data.pop('_sa_instance_state', None)
    
    return jsonify(users_data), 200

@user_bp.route("/<int:id>", methods=["GET"])
def get_by_id(id):
    user = get_user_by_id(id)
   
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user_data = user.__dict__
    user_data.pop('_sa_instance_state', None)
    
    return jsonify(user_data), 200

@user_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    data = request.get_json()

    user_data = {}

    if "telegram_id" in data:
        user_data["telegram_id"] = data.get("telegram_id")
    if "first_name" in data:
        user_data["first_name"] = data.get("first_name")
    if "username" in data:
        user_data["username"] = data.get("username")
    if "last_name" in data:
        user_data["last_name"] = data.get("last_name")

    user = update_user(id, user_data)

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user_data = user.__dict__
    user_data.pop('_sa_instance_state', None)
    
    return jsonify(user_data), 200

@user_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    user = delete_user(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"}), 204

@user_bp.route("/<int:telegram_id>/tasks", methods=["GET"])
def get_user_tasks_route(telegram_id):
    status = request.args.get("status", "")

    request_data = {}
    request_data["telegram_id"] = telegram_id
    request_data["status"] = status

    user_tasks, error = get_user_tasks(request_data)

    if error:
        return jsonify({"error": error}), 404

    return jsonify(user_tasks), 200