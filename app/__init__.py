from flask import Flask, jsonify
from flask_cors import CORS
from flask_talisman import Talisman
from flask_limiter import RateLimitExceeded

from app.common.db import db, migrate
from app.common.limiter import limiter
from app.common.middleware import handle_unexpected_error
from app.common.exceptions import CustomAPIException
from app.common.swagger import configure_swagger
from .config import config
from app.routes.category import category_bp
from app.routes.task import task_bp
from app.routes.user import user_bp

def create_app(config_mode):
    app = Flask(__name__)
    app.config.from_object(config[config_mode])
    
    CORS(app)

    csp = {
        "default-src": ["'self'", "data:"],
        "script-src": ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com"],
        "style-src": ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com"],
        "img-src": ["'self'", "data:"],
    }
    Talisman(app, content_security_policy=csp)


    limiter.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    configure_swagger(app)

    app.register_blueprint(category_bp, url_prefix="/categories")
    app.register_blueprint(task_bp, url_prefix="/tasks")
    app.register_blueprint(user_bp, url_prefix="/users")

    @app.errorhandler(CustomAPIException)
    def handle_custom_api_exception(e):
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(RateLimitExceeded)
    def rate_limit_exceeded(e):
        result = {
            "error": "Rate limit exceeded",
            "message": "You have hit the rate limit. Please try again later.",
            "limit": str(e.limit.limit),
        }
        return jsonify(result), 429

    # Error handler for 404 - Route Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"error": "Route not found"}), 404

    # Middleware for Unexpected Errors
    handle_unexpected_error(app)

    return app
