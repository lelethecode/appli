from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configurations
    db.init_app(app)  # Initialize the database with the app

    # Register blueprints or routes here

    return app
