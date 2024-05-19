import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from server.dockerManager import DockerManager

load_dotenv(".env")

db = SQLAlchemy()
dockerManager = DockerManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = "sqlite:///database.sqlite"
    )
    app.config.from_prefixed_env()

    db.init_app(app)
    dockerManager.addLogger(app.logger)

    from .webhooks import webhooks
    app.register_blueprint(webhooks)

    from .admin import admin
    app.register_blueprint(admin)

    with app.app_context():
        db.create_all()

    return app
