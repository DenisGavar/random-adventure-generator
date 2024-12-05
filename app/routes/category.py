from flask import Blueprint, jsonify, request

from app.common.exceptions import ValidationError
from app.controllers.category import (
    create_category,
    get_all_categories,
    get_category_by_id,
    update_category,
    delete_category
)

category_bp = Blueprint("categories", __name__)

@category_bp.route("/", methods=["POST"])
def create_category_route():
    data = request.get_json()

    if not data or not isinstance(data, dict):
        raise ValidationError("Invalid request body. Expected a JSON object.")
    
    required_fields = ["name"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

    request_data = {}
    request_data["name"] = data.get("name")

    result = create_category(request_data)
    return jsonify(result), 201

@category_bp.route("/", methods=["GET"])
def get_all_categories_route():
    result = get_all_categories()
    return jsonify(result), 200

@category_bp.route("/<int:id>", methods=["GET"])
def get_category_by_id_route(id):
    result = get_category_by_id(id)
    return jsonify(result), 200

@category_bp.route("/<int:id>", methods=["PUT"])
def update_category_route(id):
    data = request.get_json()

    if not data or not isinstance(data, dict):
        raise ValidationError("Invalid request body. Expected a JSON object.")
    
    request_data = {}

    if "name" in data:
        request_data["name"] = data.get("name")

    result = update_category(id, request_data)
    return jsonify(result), 200

@category_bp.route("/<int:id>", methods=["DELETE"])
def delete_category_route(id):
    result = delete_category(id)
    return jsonify(result), 204