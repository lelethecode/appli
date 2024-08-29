from flask import Flask, redirect, url_for,render_template, request, session,flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from config import app,db
from sqlalchemy import text
from sqlalchemy import MetaData
from model import Contact
from model2 import Contact2
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped,mapped_column
# app = Flask(__name__, template_folder='frontend')
# # app.secret_key = "hello"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
# # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# # app.permanent_session_lifetime = timedelta(minutes=5)
# db = SQLAlchemy(app)   
    
@app.route("/")
def home():
    return render_template("base.html")

# @app.route("/<name>")
# def user(name):
#     return f"hello {name}!"

# @app.route("/admin")
# def admin(name):
#     return redirect(url_for("user",name = "admin!"))


def xuly():
    try:
        # Fetch all users
        contacts = Contact.query.all()
        print(f"Total contacts found: {len(contacts)}")

        for contact in contacts:
            # Initialize variables to track the minimum score
            if contact.check == 0:
                min_score = float('inf')
                best_food = None

                # Fetch all food items
                foods = Contact2.query.all()
                print(f"Total foods found: {len(foods)}")

                for food in foods:
                    # Calculate the score (lower is better)
                    score = abs(contact.man - food.man) + abs(contact.ngot - food.ngot) + abs(contact.cay - food.cay)
                    print(f"Calculating score for contact {contact.username}: food {food.username} -> score: {score}")

                    # If this food has a lower score, update the minimum score variables
                    if score < min_score:
                        min_score = score
                        best_food = food.username
                        print(f"New minimum score for contact {contact.username}: food {best_food} with score {min_score}")

                # Update the user's favorite food with the food having the minimum score
                if best_food:
                    contact.favorite_food = best_food
                    print(f"Updated contact {contact.username} with favorite food {best_food}")

        # Save the results to the database
        db.session.commit()
        print("All contacts updated successfully.")

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while calculating taste: {e}")



@app.route("/run_xuly", methods=["POST"])
def run_xuly():
    xuly()  # Call the haelper function
    return jsonify({"message": "xuly function executed successfully."}), 200

# Route to display favorite foods for all users
@app.route("/food_list",methods = ["GET"])
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
        db.session.commit()
        return jsonify({"contacts": favorite_foods_list})

    except Exception as e:
        return jsonify({"message": "An error occurred while fetching favorite foods.", "error": str(e)}), 500

def schedule_tasks():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=xuly, trigger="cron", day_of_week='thu', hour=0, minute=0)
    scheduler.start()
    scheduler.add_job(func=reset_food,trigger="cron", day_of_week='sat', hour=0, minute=0)
    scheduler.start()
    
def reset_food():
    try:
        foods = Contact2.query.all()
        for food in foods:
            food.check = 0
        
        db.session.commit()
    
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while calculating taste: {e}")
        
        
@app.route("/contacts", methods=["GET"])
def get_contacts():
    try:
        contacts = Contact.query.all()
        json_contacts = [contact.to_json() for contact in contacts]
        return jsonify({"contacts": json_contacts})
    except Exception as e:
        return jsonify({"message": "An error occurred while fetching contacts.", "error": str(e)}), 500


@app.route("/create_contact", methods=["POST"])
def create_contact():
    try:
        data = request.json
        print("Received data:", data)  # Debug print
        
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        man = data.get("man")
        ngot = data.get("ngot")
        cay = data.get("cay")
        if not username or not password or not email:
            return jsonify({"message": "You must include a username and email"}), 400

        new_contact = Contact(username=username,man=man,ngot = ngot,cay = cay,email = email,password = password,check = 0)
        
        db.session.add(new_contact)
        db.session.commit()
        
        xuly()
        return jsonify({"message": "User created!"}), 201
    except Exception as e:
        print("Error:", str(e))  # Debug print
        return jsonify({"message": "An error occurred while creating the user.", "error": str(e)}), 400
    
    
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
            return jsonify({"message": "You must include a username and email"}), 400

        new_contact = Contact2(username=username,man=man,ngot = ngot,cay = cay,check = 0)
        
        db.session.add(new_contact)
        db.session.commit()
        
        return jsonify({"message": "User created!"}), 201
    except Exception as e:
        print("Error:", str(e))  # Debug print
        return jsonify({"message": "An error occurred while creating the user.", "error": str(e)}), 400


@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    contact.user_name = data.get("username", contact.user_name)
    contact.email = data.get("email", contact.email)
    contact.man = data.get("man",contact.man)
    contact.ngot = data.get("ngot",contact.ngot)
    contact.cay = data.cay("cay",contact.cay)
    contact.password = data.get("password",contact.password)
    # contact.ngot = data.get("ngot",contact.ngot)
    db.session.commit()

    return jsonify({"message": "Usr updated."}), 200


@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200

@app.route("/login", methods =["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True    
        user = request.form["nm"]
        session["user"] = user
        flash("dang nhap thanh cong")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("ban da dang nhap roi")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods = ["POST","GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("ban da nhap thanh cong email cua ban")
        else:
            if "email" in session:
                #flash("email cua ban da co san")
                email = session["email"]
        return render_template("User.html", email = email)
    else:
        flash("you not login")
        return redirect(url_for("login"))
@app.route("/logout")
def logout():
    if "user" in session: 
        user =  session["user"]
        flash(f"you have been logged out! {user}","info")
    session.pop("user",None)
    session.pop("email",None)
    return redirect(url_for("login"))


@app.route("/reset_contacts", methods=["POST"])
def reset_contacts():
    try:
        # Drop the Contact table manually
        db.session.execute(text('DROP TABLE IF EXISTS contact;'))
        db.session.commit()

        # Recreate the Contact table
        db.create_all()

        return jsonify({"message": "Contact table reset successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while resetting the contacts table.", "error": str(e)}), 500
@app.route("/reset_food_list", methods=["POST"])
def reset_food_list():
    try:
        # Drop the Contact2 table manually
        db.session.execute(text('DROP TABLE IF EXISTS contact2;'))
        db.session.commit()

        # Recreate the Contact2 table
        db.create_all()

        return jsonify({"message": "Food list reset successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while resetting the food list.", "error": str(e)}), 500
    
if __name__ == "__main__":
    with app.app_context():
        # Ensure the tables are created if they don't exist
        db.create_all()
        print("Database tables created successfully.")
    app.run(debug=True)
    app.run(host = "0.0.0.0")