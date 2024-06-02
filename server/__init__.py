from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

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
    app.config['SESSION_TYPE'] = "filesystem"
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)  # Reset session lifetime on each request

    if app.config.get('AUTH_USERNAME') is None or app.config.get('AUTH_USERNAME') is None:
        raise Exception("Missing Username and/or Password definition(s).")

    db.init_app(app)
    dockerManager.addLogger(app.logger)
    Session(app)

    from .api import api
    app.register_blueprint(api)

    from .admin import admin
    app.register_blueprint(admin)

    from .auth import auth
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()

    return app
