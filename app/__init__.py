from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman

from app.common.db import db, migrate
from .config import config
from app.routes.category import category_bp
from app.routes.task import task_bp

def create_app(config_mode):
    app = Flask(__name__)
    app.config.from_object(config[config_mode])
    
    CORS(app)
    Talisman(app)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(category_bp, url_prefix="/categories")
    app.register_blueprint(task_bp, url_prefix="/tasks")

    return app
