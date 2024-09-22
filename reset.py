from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configure your app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://leledatabase_user:gllglkTmoT3sZmkWp1HzboT2AsYXeW5a@dpg-cr811g3tq21c739hlq40-a.oregon-postgres.render.com/leledatabase'  # Update with your actual database URI
db = SQLAlchemy(app)

# Import your models
class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    check = db.Column(db.Integer)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    man = db.Column(db.Integer)
    ngot = db.Column(db.Integer)
    cay = db.Column(db.Integer)
    favorite_food = db.Column(db.String(120))
    favorite_food_t2 = db.Column(db.String(120))
    favorite_food_t3 = db.Column(db.String(120))
    favorite_food_t4 = db.Column(db.String(120))
    favorite_food_t5 = db.Column(db.String(120))
    favorite_food_t6 = db.Column(db.String(120))

# Drop all tables and create new ones
with app.app_context():
    db.drop_all()   # Drop all existing tables
    db.create_all()  # Create tables as per the models defined

print("Database reset completed.")
