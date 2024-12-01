from flask import Blueprint, jsonify, request
from app.controllers.category import create_category

category_bp = Blueprint("categories", __name__)

@category_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400
    category = create_category({"name": name})
    return jsonify({"id": category.id, "name": category.name}), 201