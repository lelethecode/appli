from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configure your app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://leledatabase_zj8a_user:UhlqQO3FKIcYYbxnzfbR7CjA6KOkX94W@dpg-crrq63l6l47c73cmphm0-a.oregon-postgres.render.com/leledatabase_zj8a'  # Update with your actual database URI
db = SQLAlchemy(app)

# Import your models
class Contact2(db.Model):
    __tablename__ = 'contact2'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120),nullable = False,unique = True)
    check = db.Column(db.Integer, default=0)
    man = db.Column(db.Integer)
    ngot = db.Column(db.Integer)
    cay = db.Column(db.Integer)

# Drop all tables and create new ones
with app.app_context():
    db.drop_all()   # Drop all existing tables
    db.create_all()  # Create tables as per the models defined

print("Database reset completed.")
