from flask import Blueprint, jsonify, request
from app.controllers.category import create_category, get_all_categories, get_category_by_id, update_category, delete_category

category_bp = Blueprint("categories", __name__)

@category_bp.route("/", methods=["POST"])
def create():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    category = create_category({"name": name})
    return jsonify({"id": category.id, "name": category.name}), 201

@category_bp.route("/", methods=["GET"])
def get_all():
    categories = get_all_categories()
    return jsonify([{"id": category.id, "name": category.name} for category in categories]), 200

@category_bp.route("/<int:id>", methods=["GET"])
def get_by_id(id):
    category = get_category_by_id(id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify({"id": category.id, "name": category.name}), 200

@category_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400
        
    category = update_category(id, data)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify({"id": category.id, "name": category.name}), 200

@category_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    category = delete_category(id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify({"message": "Category deleted successfully"}), 204