from flask import Blueprint, jsonify, request

from app.common.limiter import limiter
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
    """
    Create a new task
    ---
    tags:
      - Tasks
    requestBody:
      description: JSON object containing the task description and category
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              description:
                type: string
                example: "Write a letter to your future self."
              category:
                type: string
                example: "Personal"
            required:
              - description
              - category
    responses:
      201:
        description: Successfully created a new task
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                description:
                  type: string
                  example: "Write a letter to your future self."
                category:
                  type: string
                  example: "Personal"
      400:
        description: Validation error (missing required fields or invalid input)
      500:
        description: Internal server error
    """
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
    """
    Get a list of all tasks
    ---
    tags:
      - Tasks
    responses:
      200:
        description: List of all tasks
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
                  description:
                    type: string
                    example: "Write a letter to your future self."
                  category:
                    type: string
                    example: "Personal"
      500:
        description: Internal server error
    """
    result = get_all_tasks()
    return jsonify(result), 200

@task_bp.route("/<int:id>", methods=["GET"])
def get_task_by_id_route(id):
    """
    Get a task by ID
    ---
    tags:
      - Tasks
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
          example: 1
        description: ID of the task
    responses:
      200:
        description: Task details
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                description:
                  type: string
                  example: "Write a letter to your future self."
                category:
                  type: string
                  example: "Personal"
      404:
        description: Task not found
      500:
        description: Internal server error
    """
    result = get_task_by_id(id)
    return jsonify(result), 200

@task_bp.route("/<int:id>", methods=["PUT"])
def update_task_route(id):
    """
    Update a task by ID
    ---
    tags:
      - Tasks
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
          example: 1
        description: ID of the task to update
    requestBody:
      description: JSON object containing the task description and/or category to update
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              description:
                type: string
                example: "Update the description of the task."
              category:
                type: string
                example: "Work"
    responses:
      200:
        description: Successfully updated task
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                description:
                  type: string
                  example: "Update the description of the task."
                category:
                  type: string
                  example: "Work"
      400:
        description: Validation error (missing required fields or invalid input)
      404:
        description: Task not found
      500:
        description: Internal server error
    """
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
    """
    Delete a task by ID
    ---
    tags:
      - Tasks
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
          example: 1
        description: ID of the task to delete
    responses:
      204:
        description: Successfully deleted task
      404:
        description: Task not found
      500:
        description: Internal server error
    """
    result = delete_task(id)
    return jsonify(result), 204

def telegram_id_key():
    data = request.get_json()
    telegram_id = str(data.get("telegram_id", "anonymous"))
    return telegram_id

@task_bp.route("/generate", methods=["POST"])
@limiter.limit("3 per minute", key_func=telegram_id_key)
@limiter.limit("5 per hour", key_func=telegram_id_key)
def generate_task_route():
    """
    Generate a new task
    ---
    tags:
      - Tasks
    requestBody:
      description: JSON object containing the category and telegram_id to generate a task
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              telegram_id:
                type: integer
                example: 123456789
              category:
                type: string
                example: "Personal"
            required:
              - telegram_id
    responses:
      200:
        description: Task generated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                description:
                  type: string
                  example: "Write a letter to your future self."
                category:
                  type: string
                  example: "Personal"
      400:
        description: Validation error (missing required fields or invalid input)
      404:
        description: Category or user not found
      500:
        description: Internal server error
    """
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
    """
    Assign an existing task to a user
    ---
    tags:
      - Tasks
    requestBody:
      description: JSON object containing the telegram_id and optionally a category to assign an existing task
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              telegram_id:
                type: integer
                example: 123456789
              category:
                type: string
                example: "Work"
            required:
              - telegram_id
    responses:
      200:
        description: Successfully assigned an existing task to the user
        content:
          application/json:
            schema:
              type: object
              properties:
                task_id:
                  type: integer
                  example: 1
                description:
                  type: string
                  example: "Finish the project report"
                category:
                  type: string
                  example: "Work"
      400:
        description: Validation error (missing required fields or invalid input)
      404:
        description: No task found to assign for the specified category
      500:
        description: Internal server error
    """
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
    """
    Complete a task
    ---
    tags:
      - Tasks
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
          example: 1
        description: ID of the task to complete
    requestBody:
      description: JSON object containing the telegram_id to mark the task as complete
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              telegram_id:
                type: integer
                example: 123456789
            required:
              - telegram_id
    responses:
      200:
        description: Task marked as complete
      404:
        description: Task or user not found
      500:
        description: Internal server error
    """
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