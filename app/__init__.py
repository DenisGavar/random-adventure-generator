from flask import Flask

from app.common.db import db, migrate
from .config import config
from app.routes.category import category_bp

def create_app(config_mode):
    app = Flask(__name__)
    app.config.from_object(config[config_mode])

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(category_bp, url_prefix="/categories")

    return app
