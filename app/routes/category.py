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
    """
    Create a new category
    ---
    tags:
      - Categories
    requestBody:
      description: JSON object containing the category name
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                example: "Sport"
            required:
              - name
    responses:
      201:
        description: Successfully created a new category
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: "Sport"
      400:
        description: Validation error (missing required fields or invalid input)
      500:
        description: Internal server error
    """
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
    """
    Get a list of all categories
    ---
    tags:
      - Categories
    responses:
      200:
        description: List of all categories
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: "Sport"
                type: object
                properties:
                  id:
                    type: integer
                    example: 2
                  name:
                    type: string
                    example: "Cooking"
      500:
        description: Internal server error
    """
    result = get_all_categories()
    return jsonify(result), 200

@category_bp.route("/<int:id>", methods=["GET"])
def get_category_by_id_route(id):
    """
    Get a category by ID
    ---
    tags:
      - Categories
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
          example: 1
        description: ID of the category
    responses:
      200:
        description: Category details
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: "Sport"
      404:
        description: Category not found
      500:
        description: Internal server error
    """
    result = get_category_by_id(id)
    return jsonify(result), 200

@category_bp.route("/<int:id>", methods=["PUT"])
def update_category_route(id):
    """
    Update a category by ID
    ---
    tags:
      - Categories
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
          example: 1
        description: ID of the category to update
    requestBody:
      description: JSON object containing the updated category details
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                example: "New Category Name"
    responses:
      200:
        description: Updated category details
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: "New Category Name"
      404:
        description: Category not found
      400:
        description: Validation error (missing required fields or invalid input)
      500:
        description: Internal server error
    """
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
    """
    Delete a category by ID
    ---
    tags:
      - Categories
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
          example: 1
        description: ID of the category to delete
    responses:
      204:
        description: Category successfully deleted
      404:
        description: Category not found
      500:
        description: Internal server error
    """
    result = delete_category(id)
    return jsonify(result), 204