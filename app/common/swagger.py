from flasgger import Swagger
import os
from dotenv import load_dotenv

load_dotenv(override=True)

def configure_swagger(app):
    """
    Configure Swagger documentation for the app.
    """
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "swagger",
                "route": "/swagger.json",
                "rule_filter": lambda rule: True,  # Include all endpoints
                "model_filter": lambda tag: True,  # Include all tags
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Random Adventure Generator API",
            "description": "API documentation for Random Adventure Generator",
            "version": "1.0.0",
        },
        "host": os.getenv("HOST"),
        "basePath": "/",
    }

    Swagger(app, config=swagger_config, template=swagger_template)
