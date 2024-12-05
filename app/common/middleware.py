from flask import jsonify

def handle_unexpected_error(app):
    @app.errorhandler(Exception)
    def handle_generic_error(e):
        app.logger.error(f"Unexpected error: {str(e)}")

        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
