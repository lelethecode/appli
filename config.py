import os

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql import func
app = Flask(__name__,template_folder="frontend")
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:lele9920483@localhost:5432/model'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#postgresql://leledatabase_user:gllglkTmoT3sZmkWp1HzboT2AsYXeW5a@dpg-cr811g3tq21c739hlq40-a.oregon-postgres.render.com/leledatabase


db = SQLAlchemy(app)