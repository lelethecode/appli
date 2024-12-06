import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
# Initialize the database and migration objects
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_folder="frontend/build", template_folder="frontend")
    migrate = Migrate(app, db)
    CORS(app)

    # Configuration settings
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatatbase.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://leledatabase_5193_user:kvi1DnTAlwSDg3tP5zKgAYqKh2NIE4MF@dpg-ct9bl01opnds73e6uia0-a.oregon-postgres.render.com/leledatabase_5193'
    #gllglkTmoT3sZmkWp1HzboT2AsYXeW5a
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv('SECRET_KEY', 'lelethecoder')  # Set your secret key
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register your blueprints or routes here if you have any

    return app
