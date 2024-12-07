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
    """
    Create a new user
    ---
    tags:
      - Users
    requestBody:
      description: JSON object containing the user details
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              telegram_id:
                type: integer
                example: 123456789
              first_name:
                type: string
                example: "John"
              username:
                type: string
                example: "john_doe"
              last_name:
                type: string
                example: "Doe"
            required:
              - telegram_id
              - first_name
    responses:
      201:
        description: Successfully created a new user
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                telegram_id:
                  type: integer
                  example: 123456789
                first_name:
                  type: string
                  example: "John"
                username:
                  type: string
                  example: "john_doe"
                last_name:
                  type: string
                  example: "Doe"
      400:
        description: Validation error (missing required fields or invalid input)
      500:
        description: Internal server error
    """
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
    """
    Get a list of all users
    ---
    tags:
      - Users
    responses:
      200:
        description: List of all users
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
                  telegram_id:
                    type: integer
                    example: 123456789
                  first_name:
                    type: string
                    example: "John"
                  username:
                    type: string
                    example: "john_doe"
                  last_name:
                    type: string
                    example: "Doe"
      500:
        description: Internal server error
    """

    result = get_all_users()
    return jsonify(result), 200

@user_bp.route("/<int:id>", methods=["GET"])
def get_user_by_id_route(id):
    """
    Get a user by ID
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
          example: 1
        description: ID of the user
    responses:
      200:
        description: User details
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                telegram_id:
                  type: integer
                  example: 123456789
                first_name:
                  type: string
                  example: "John"
                username:
                  type: string
                  example: "john_doe"
                last_name:
                  type: string
                  example: "Doe"
      404:
        description: User not found
      500:
        description: Internal server error
    """
    result = get_user_by_id(id)
    return jsonify(result), 200

@user_bp.route("/<int:id>", methods=["PUT"])
def update_user_route(id):
    """
    Update a user by ID
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
          example: 1
        description: ID of the user to update
    requestBody:
      description: JSON object containing the updated user details
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              telegram_id:
                type: integer
                example: 123456789
              first_name:
                type: string
                example: "John"
              username:
                type: string
                example: "john_doe"
              last_name:
                type: string
                example: "Doe"
    responses:
      200:
        description: Updated user details
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                telegram_id:
                  type: integer
                  example: 123456789
                first_name:
                  type: string
                  example: "John"
                username:
                  type: string
                  example: "john_doe"
                last_name:
                  type: string
                  example: "Doe"
      404:
        description: User not found
      400:
        description: Validation error (missing required fields or invalid input)
      500:
        description: Internal server error
    """
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
    """
    Delete a user by ID
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
          example: 1
        description: ID of the user to delete
    responses:
      204:
        description: User successfully deleted
      404:
        description: User not found
      500:
        description: Internal server error
    """
    result = delete_user(id)
    return jsonify(result), 204

@user_bp.route("/<int:telegram_id>/tasks", methods=["GET"])
def get_user_tasks_route(telegram_id):
    """
    Get tasks for a user by telegram_id
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: telegram_id
        required: true
        schema:
          type: integer
          example: 123456789
        description: ID of the user
      - in: query
        name: status
        required: false
        schema:
          type: string
          example: "completed"
        description: Filter tasks by status (optional)
    responses:
      200:
        description: List of tasks for the user
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  task_id:
                    type: integer
                    example: 1
                  description:
                    type: string
                    example: "Complete adventure quest"
                  category_name:
                    type: string
                    example: "Sport"
                  status:
                    type: string
                    example: "completed"
                  assigned_at:
                    type: string
                    example: "2024-12-01T12:00:00"
                  completed_at:
                    type: string
                    example: "2024-12-02T12:00:00"
      404:
        description: User not found
      500:
        description: Internal server error
    """
    status = request.args.get("status", "")

    request_data = {}
    request_data["telegram_id"] = telegram_id
    request_data["status"] = status

    result = get_user_tasks(request_data)
    return jsonify(result), 200