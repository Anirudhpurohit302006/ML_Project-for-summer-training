from flask import Flask
from app.config import Config
from app.extensions import db, login_manager
from app.routes import register_routes
from app.models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    register_routes(app)

    with app.app_context():
        db.create_all()

    return app