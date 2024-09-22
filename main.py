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
from flask_cors import CORS, cross_origin
from werkzeug.security import check_password_hash
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
            if contact.check == False:
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
        
def xulydon(user_id):
    try:
        # Query the contact with the given user_id
        contact = Contact.query.get(user_id)
        if contact is None:
            print(f"No contact found with user_id {user_id}")
            return

        print(f"Calculating favorite food for contact {contact.username}")

        if contact.check == False:
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
                contact.check = True  # Mark the contact as having calculated favorite food
                print(f"Updated contact {contact.username} with favorite food {best_food}")

        db.session.commit()
        print(f"Contact {contact.username} updated successfully.")

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while calculating favorite food for contact {contact.username}: {e}")

@app.route("/run_xuly", methods=["POST"])
def run_xuly():
    xuly()  # Call the helper function
    return jsonify({"message": "xuly function executed successfully."}), 200


def run_xulydon(user_id):
    xulydon(user_id)  # Call the function with the specific user ID
    return jsonify({"message": f"xulydon function executed successfully for user {user_id}."}), 200

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
                "favorite_food": favorite_food,
                "check":contact.check
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

@app.route('/foodlist', methods=['GET'])
def get_food():
    # Query the database for the food items
    food_items = Contact2.query.all()
    
    # Prepare the data in JSON format
    food_list = [{
        'id': food.id,
        'name': food.username,  # Assuming username is the name of the food
        'image_url': f'/images/{food.username}.jpg'  # Assuming images are named after the food
    } for food in food_items]
    
    return jsonify(food_list)

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
        favorite_food=data.get('favorite_food'),  # Optional field
        favorite_food_t2=data.get('favorite_food_t2'),
        favorite_food_t3=data.get('favorite_food_t3'),
        favorite_food_t4=data.get('favorite_food_t4'),
        favorite_food_t5=data.get('favorite_food_t5'),
        favorite_food_t6=data.get('favorite_food_t6'),
        check = False
    )

    # Save to the database
    try:
        db.session.add(new_contact)
        db.session.commit()
        xulydon(new_contact.id)
        return jsonify({"message": "Contact created successfully."}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/get_food_list", methods=["GET"])
def get_food_list():
    try:
        food_items = Contact2.query.all()
        food_list = [{"id": food.id, "name": food.username} for food in food_items]
        return jsonify(food_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/create_food", methods=["POST"])
def create_food():
    data = request.json

    username = data.get('username')
    man = data.get('man')
    ngot = data.get('ngot')
    cay = data.get('cay')
    check = data.get('check', False)  # Giá trị mặc định là False nếu không có trong yêu cầu

    # Chuyển đổi giá trị check từ 0/1 sang True/False
    if isinstance(check, int):
        check = bool(check)

    # Kiểm tra các trường có tồn tại không
    if username is None or man is None or ngot is None or cay is None:
        return jsonify({"message": "Thông tin không hợp lệ"}), 400

    # Kiểm tra kiểu dữ liệu
    if not isinstance(man, int) or not isinstance(ngot, int) or not isinstance(cay, int):
        return jsonify({"message": "Các trường 'man', 'ngot', và 'cay' phải là số nguyên"}), 400

    # Thực hiện việc lưu vào cơ sở dữ liệu
    new_food = Contact2(username=username, man=man, ngot=ngot, cay=cay, check=check)
    db.session.add(new_food)
    db.session.commit()

    return jsonify({"message": "Thêm món ăn thành công!"}), 201

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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Parses the JSON data from the request
    username = data.get('username')
    password = data.get('password')

    if not username or password is None:
        return jsonify({"success": False, "message": "Username and password are required."}), 400

    # Find the user by username
    user = Contact.query.filter_by(username=username).first()

    if user is None:
        return jsonify({"success": False, "message": "Invalid username or password."}), 401

    # Replace check_password_hash with a simple comparison
    if user.password != password:  # Replace this line with your logic
        return jsonify({"success": False, "message": "Invalid username or password."}), 401

    # If the password is correct
    session['user_id'] = user.id
    return jsonify({"success": True, "message": "Login successful", "user": user.to_json()})



@app.route("/logout")
def logout():
    if "user" in session: 
        user = session["user"]
        flash(f"Bạn đã đăng xuất! {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))
@app.route('/delete_contact_table', methods=['DELETE'])
def delete_contact_table():
    db.engine.execute("DROP TABLE IF EXISTS contact;")
    return jsonify({"message": "Contact table deleted successfully!"}), 200

if __name__ == "__main__":
    #schedule_tasks()  # Start scheduled tasks
    app.run(host="0.0.0.0", port=5000, debug=True)
