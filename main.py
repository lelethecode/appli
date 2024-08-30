import os
from sqlite3 import IntegrityError
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import text
from model import Contact
from model2 import Contact2
from datetime import timedelta
from config import create_app, db  # Ensure this imports correctly
from flask_migrate import Migrate

# db = SQLAlchemy()
# migrate = Migrate()
# app = Flask(__name__)

# # Configuration settings
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://leledatabase_user:lele9920483@dpg-cr811g3tq21c739hlq40-a/leledatabase')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# #app.secret_key = os.getenv('SECRET_KEY', 'lelethecoder')  # Set your secret key

# # Initialize extensions
# db.init_app(app)
# migrate.init_app(app, db)  # Create the app instance
app = create_app()

@app.route("/")
def home():
    return render_template("base.html")

# Define the xuly function
def xuly():
    try:
        contacts = Contact.query.all()
        print(f"Total contacts found: {len(contacts)}")

        for contact in contacts:
            if contact.check == 0:
                min_score = float('inf')
                best_food = None

                foods = Contact2.query.all()
                print(f"Total foods found: {len(foods)}")

                for food in foods:
                    score = abs(contact.man - food.man) + abs(contact.ngot - food.ngot) + abs(contact.cay - food.cay)
                    print(f"Calculating score for contact {contact.username}: food {food.username} -> score: {score}")

                    if score < min_score:
                        min_score = score
                        best_food = food.username
                        print(f"New minimum score for contact {contact.username}: food {best_food} with score {min_score}")

                if best_food:
                    contact.favorite_food = best_food
                    print(f"Updated contact {contact.username} with favorite food {best_food}")

        db.session.commit()
        print("All contacts updated successfully.")

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while calculating taste: {e}")

@app.route("/run_xuly", methods=["POST"])
def run_xuly():
    xuly()  # Call the helper function
    return jsonify({"message": "xuly function executed successfully."}), 200

# Route to display favorite foods for all users
@app.route("/food_list", methods=["GET"])
def food_list():
    try:
        contacts = Contact2.query.all()
        json_contacts = [contact.to_json() for contact in contacts]
        return jsonify({"contacts": json_contacts})
    except Exception as e:
        return jsonify({"message": "An error occurred while fetching contacts.", "error": str(e)}), 500

@app.route("/favorite_foods", methods=["GET"])
def favorite_foods():
    try:
        contacts = Contact.query.all()
        favorite_foods_list = []

        for contact in contacts:
            favorite_food = contact.favorite_food or "None"
            favorite_foods_list.append({
                "user_id": contact.id,
                "username": contact.username,
                "favorite_food": favorite_food
            })

        return jsonify({"contacts": favorite_foods_list})

    except Exception as e:
        return jsonify({"message": "An error occurred while fetching favorite foods.", "error": str(e)}), 500

def schedule_tasks():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=xuly, trigger="cron", day_of_week='thu', hour=0, minute=0)
    scheduler.start()
    scheduler.add_job(func=reset_food, trigger="cron", day_of_week='sat', hour=0, minute=0)

def reset_food():
    try:
        foods = Contact2.query.all()
        for food in foods:
            food.check = 0
        
        db.session.commit()
    
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while resetting food: {e}")

@app.route("/contacts", methods=["GET"])
def get_contacts():
    try:
        contacts = Contact.query.all()
        json_contacts = [contact.to_json() for contact in contacts]
        return jsonify({"contacts": json_contacts})
    except Exception as e:
        return jsonify({"message": "An error occurred while fetching contacts.", "error": str(e)}), 500

@app.route('/create_contact', methods=['POST'])
def create_contact():
    data = request.get_json()

    # Validate required fields
    required_fields = ['username', 'password', 'email', 'man', 'ngot', 'cay']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"{field} is required."}), 400

    # Validate 'man', 'ngot', 'cay' are integers between 1 and 3
    for field in ['man', 'ngot', 'cay']:
        if not isinstance(data[field], int) or not (1 <= data[field] <= 3):
            return jsonify({"error": f"{field} must be an integer between 1 and 3."}), 400

    # Create a new contact instance
    new_contact = Contact(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        man=data['man'],
        ngot=data['ngot'],
        cay=data['cay'],
        favorite_food=data.get('favorite_food')  # Optional field
    )

    # Save to the database
    try:
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({"message": "Contact created successfully."}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@app.route("/create_food", methods=["POST"])
def create_food():
    try:
        data = request.json
        print("Received data:", data)  # Debug print
        
        username = data.get("username")
        man = data.get("man")
        ngot = data.get("ngot")
        cay = data.get("cay")
        if not username:
            return jsonify({"message": "You must include a username"}), 400

        new_food = Contact2(username=username, man=man, ngot=ngot, cay=cay, check=0)
        
        db.session.add(new_food)
        db.session.commit()
        
        return jsonify({"message": "Food created!"}), 201
    except Exception as e:
        print("Error:", str(e))  # Debug print
        return jsonify({"message": "An error occurred while creating the food.", "error": str(e)}), 400

@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    contact.username = data.get("username", contact.username)
    contact.email = data.get("email", contact.email)
    contact.man = data.get("man", contact.man)
    contact.ngot = data.get("ngot", contact.ngot)
    contact.cay = data.get("cay", contact.cay)
    contact.password = data.get("password", contact.password)

    db.session.commit()

    return jsonify({"message": "User updated."}), 200

@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True    
        user = request.form["nm"]
        session["user"] = user
        flash("Đăng nhập thành công")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Bạn đã đăng nhập rồi")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Bạn đã nhập thành công email của bạn")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("User.html", email=email)
    else:
        flash("Bạn chưa đăng nhập")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session: 
        user = session["user"]
        flash(f"Bạn đã đăng xuất! {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    #schedule_tasks()  # Start scheduled tasks
    app.run(debug=True)  # Start the Flask application
    app.run(host = "0.0.0.0")
