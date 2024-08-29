import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
# Initialize the database and migration objects
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
    # Configuration settings
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatatbase.db"
    #app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://leledatabase_user:gllglkTmoT3sZmkWp1HzboT2AsYXeW5a@dpg-cr811g3tq21c739hlq40-a.oregon-postgres.render.com/leledatabase')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv('SECRET_KEY', 'lelethecoder')  # Set your secret key

    # Initialize extensions
    cors = CORS(app, resources={r"http://localhost:5173/": {"origins": "*"}})
    db.init_app(app)
    migrate.init_app(app, db)

    # Register your blueprints or routes here if you have any

    return app
