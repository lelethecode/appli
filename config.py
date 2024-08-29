import os

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql import func
class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'lelethecoder ')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:lele9920483@localhost:5432/model')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Create the Flask app
app = Flask(__name__, template_folder="frontend")
app.config.from_object(Config)

# Initialize CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Initialize SQLAlchemy
db = SQLAlchemy(app)