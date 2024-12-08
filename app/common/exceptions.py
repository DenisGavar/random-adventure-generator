class CustomAPIException(Exception):
    status_code = 400  # Default status code

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {"error": self.message}


class DatabaseError(CustomAPIException):
    """Exception for database-related errors."""
    status_code = 500


class NotFoundError(CustomAPIException):
    """Exception for resource not found."""
    status_code = 404


class ValidationError(CustomAPIException):
    """Exception for validation errors."""
    status_code = 400

class AIGenerationError(CustomAPIException):
    """Exception for AI generation."""
    status_code = 500

class AlreadyExistsError(CustomAPIException):
    """Exception for entity already exists."""
    status_code = 409
