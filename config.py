import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'lelethecoder')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:lele9920483@localhost:5432/model')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def create_app():
    app = Flask(__name__, template_folder="frontend")
    app.config.from_object(Config)

    # Initialize CORS
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    # Initialize SQLAlchemy
    db.init_app(app)

    with app.app_context():
        # Ensure the tables are created if they don't exist
        db.create_all()

    return app
