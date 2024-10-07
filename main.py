import os
from sqlite3 import IntegrityError
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify,json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import text
from model import Contact
from model2 import Contact2
from datetime import timedelta
from config import create_app, db  
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from werkzeug.security import check_password_hash
app = create_app()

@app.route("/")
def home():
    return render_template("base.html")

def xuly():
    try:
        contacts = Contact.query.all()
        print(f"Total contacts found: {len(contacts)}")

        for contact in contacts:
            if contact.check == 0:
                min_score2 = float('inf')
                min_score3 = float('inf')
                min_score4 = float('inf')
                min_score5 = float('inf')
                min_score6 = float('inf')
                best_food2 = None
                best_food3 = None
                best_food4 = None
                best_food5 = None
                best_food6 = None

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
        contact = Contact.query.get(user_id)
        if contact is None:
            print(f"No contact found with user_id {user_id}")
            return

        print(f"Calculating favorite food for contact {contact.username}")

        if contact.check != 1:
            min_score = float('inf')
            best_food = None
            min_score2 = float('inf')
            min_score3 = float('inf')
            min_score4 = float('inf')
            min_score5 = float('inf')
            min_score6 = float('inf')
            best_food2 = None
            best_food3 = None
            best_food4 = None
            best_food5 = None
            best_food6 = None

            foods = Contact2.query.all()
            print(f"Total foods found: {len(foods)}")

            for food in foods:
                if food.check == 2:
                    score = abs(contact.man - food.man) + abs(contact.ngot - food.ngot) + abs(contact.cay - food.cay)
                    print(f"Calculating score for contact {contact.username}: food {food.username} -> score: {score}")

                    if score < min_score2:
                        min_score2 = score
                        best_food2 = food.username
                        print(f"New minimum score for contact {contact.username}: food {best_food} with score {min_score}")
                    if best_food:
                        contact.favorite_food_t2 = best_food2
                        contact.check = 1 
                        print(f"Updated contact {contact.username} with favorite food {best_food}")
                if food.check == 3:
                    score = abs(contact.man - food.man) + abs(contact.ngot - food.ngot) + abs(contact.cay - food.cay)
                    print(f"Calculating score for contact {contact.username}: food {food.username} -> score: {score}")

                    if score < min_score3:
                        min_score3 = score
                        best_food3 = food.username
                        print(f"New minimum score for contact {contact.username}: food {best_food} with score {min_score}")
                    if best_food:
                        contact.favorite_food_t3 = best_food3
                        contact.check = 1
                        print(f"Updated contact {contact.username} with favorite food {best_food}")
                if food.check == 4:
                    score = abs(contact.man - food.man) + abs(contact.ngot - food.ngot) + abs(contact.cay - food.cay)
                    print(f"Calculating score for contact {contact.username}: food {food.username} -> score: {score}")

                    if score < min_score4:
                        min_score4 = score
                        best_food4 = food.username
                        print(f"New minimum score for contact {contact.username}: food {best_food} with score {min_score}")
                    if best_food:
                        contact.favorite_food_t4 = best_food4
                        contact.check = 1 
                        print(f"Updated contact {contact.username} with favorite food {best_food}")
                if food.check == 5:
                    score = abs(contact.man - food.man) + abs(contact.ngot - food.ngot) + abs(contact.cay - food.cay)
                    print(f"Calculating score for contact {contact.username}: food {food.username} -> score: {score}")

                    if score < min_score5:
                        min_score5 = score
                        best_food5 = food.username
                        print(f"New minimum score for contact {contact.username}: food {best_food} with score {min_score}")
                    if best_food:
                        contact.favorite_food_t5 = best_food5
                        contact.check = 1 
                        print(f"Updated contact {contact.username} with favorite food {best_food}")
                if food.check == 6:
                    score = abs(contact.man - food.man) + abs(contact.ngot - food.ngot) + abs(contact.cay - food.cay)
                    print(f"Calculating score for contact {contact.username}: food {food.username} -> score: {score}")

                    if score < min_score6:
                        min_score6 = score
                        best_food6 = food.username
                        print(f"New minimum score for contact {contact.username}: food {best_food} with score {min_score}")
                    if best_food:
                        contact.favorite_food_t6 = best_food6
                        contact.check = 1  
                        print(f"Updated contact {contact.username} with favorite food {best_food}")

        db.session.commit()
        print(f"Contact {contact.username} updated successfully.")

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while calculating favorite food for contact {contact.username}: {e}")

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    userid = json.loads(data['user_id'])
    feedback = data['feedback']

    # Logic to save feedback to the database
    contact = Contact.query.filter_by(id = userid["id"]).first()
    if contact:
        contact.feedback = feedback  # Save the feedback
        db.session.commit()
        return jsonify({"message": "Feedback submitted successfully!"}), 200
    else:
        return jsonify({"message": "User not found."}), 404
    

@app.route('/choose_food_week', methods=['POST'])
def choose_food_week():
    data = request.get_json()
    selected_foods = data.get('selected_foods')  # This is a list of dicts [{'foodId': 1, 'dayCheck': 2}, ...]

    if not selected_foods:
        return jsonify({"message": "No food selected"}), 400

    try:
        for item in selected_foods:
            # Extract foodId and dayCheck from the dictionary
            food_id = int(item.get('foodId'))  # Convert foodId to an integer
            day_check = int(item.get('dayCheck'))  # dayCheck is already an integer

            # Debugging output
            print(f"Processing food_id: {food_id}, day_check: {day_check}")

            # Query the Contact2 table to find the food item by its ID
            food = Contact2.query.filter_by(id=food_id).first()

            if food:
                # Update the 'check' field based on day_check
                food.check = day_check
            else:
                # If the food item is not found, return an error message
                return jsonify({"message": f"Food with id {food_id} not found"}), 404

        # Commit all changes to the database after the loop
        db.session.commit()
        return jsonify({"message": "Food selection updated successfully"}), 200

    except Exception as e:
        # Rollback any changes in case of an error
        db.session.rollback()
        return jsonify({"message": "Failed to update food selection", "error": str(e)}), 500


@app.route('/choose_food', methods=['POST'])
def choose_food():
    data = request.get_json()
    selected_foods = data['selected_foods'] 
    userid = json.loads(data['user_id'])
    print(userid)
    if not selected_foods:
        return jsonify({"message": "No food selected"}), 400

    try:
       
        
        for food_id, check_value in selected_foods.items():

            print(userid["id"])
            food = Contact.query.filter_by(id = userid["id"]).first()
            if food:
                if food_id == 'monday':
                    food.favorite_food_t2 = check_value
                if food_id == 'tuesday':
                    food.favorite_food_t3 = check_value
                if food_id == 'wednesday':
                    food.favorite_food_t4 = check_value
                if food_id == 'thursday':
                    food.favorite_food_t5 = check_value
                if food_id == 'friday':
                    food.favorite_food_t6 = check_value
                food.check = 1

        db.session.commit()
        return jsonify({"message": "Food selection updated successfully"}), 200

    except Exception as e:
        #print(userid)
        return jsonify({"message": "Failed to update food selection"}), 500

    
@app.route("/run_xuly", methods=["POST"])
def run_xuly():
    xuly()  
    return jsonify({"message": "xuly function executed successfully."}), 200


def run_xulydon(user_id):
    xulydon(user_id) 
    return jsonify({"message": f"xulydon function executed successfully for user {user_id}."}), 200


@app.route("/food_list", methods=["GET"])
def food_list():
    try:
        contacts = Contact2.query.all()
        json_contacts = [contact.to_json() for contact in contacts]
        return jsonify({"contacts": json_contacts})
    except Exception as e:
        return jsonify({"message": "An error occurred while fetching contacts.", "error": str(e)}), 500

@app.route('/favorite-food', methods=['GET'])
def get_favorite_food():
    user_id = request.args.get('user_id')
    print(user_id)  
    contact = Contact.query.filter_by(id=user_id).first()
    if contact:
        return jsonify({
            't2': contact.favorite_food_t2,
            't3': contact.favorite_food_t3,
            't4': contact.favorite_food_t4,
            't5': contact.favorite_food_t5,
            't6': contact.favorite_food_t6,
        })
    else:
        return jsonify({'error': 'User not found'}), 404



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
    food_items = Contact2.query.all()
    
    food_list = [{
        'id': food.id,
        'name': food.username,  
        'image_url': f'/images/{food.username}.jpg' 
    } for food in food_items]
    
    return jsonify(food_list)

@app.route('/create_contact', methods=['POST'])
def create_contact():
    data = request.get_json()

    required_fields = ['username', 'password', 'email', 'man', 'ngot', 'cay']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"{field} is required."}), 400

    for field in ['man', 'ngot', 'cay']:
        if not isinstance(data[field], int) or not (0 <= data[field] <= 100):
            return jsonify({"error": f"{field} must be an integer between 1 and 3."}), 400

    new_contact = Contact(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        man=data['man'],
        ngot=data['ngot'],
        cay=data['cay'],
        favorite_food=data.get('favorite_food'),  
        favorite_food_t2=data.get('favorite_food_t2'),
        favorite_food_t3=data.get('favorite_food_t3'),
        favorite_food_t4=data.get('favorite_food_t4'),
        favorite_food_t5=data.get('favorite_food_t5'),
        favorite_food_t6=data.get('favorite_food_t6'),
        check = 0
    )

    
    try:
        db.session.add(new_contact)
        db.session.commit()
        run_xulydon(new_contact.id)
        return jsonify({"message": "Contact created successfully."}), 201
    except IntegrityError as e:
        db.session.rollback()
        print(f"IntegrityError: {e}")  
        return jsonify({"error": "Username or email already exists."}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/get_food_list", methods=["GET"])
def get_food_list():
    try:
        food_items = Contact2.query.all()
        food_list = [{"id": food.id, "name": food.username, "check": food.check} for food in food_items]
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
    check = data.get('check', 0)  


    if username is None or man is None or ngot is None or cay is None:
        return jsonify({"message": "Thông tin không hợp lệ"}), 400

    if not isinstance(man, int) or not isinstance(ngot, int) or not isinstance(cay, int):
        return jsonify({"message": "Các trường 'man', 'ngot', và 'cay' phải là số nguyên"}), 400

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
    data = request.get_json()  
    username = data.get('username')
    password = data.get('password')
    print(username)
    if not username or password is None:
        return jsonify({"success": False, "message": "Username and password are required."}), 400

    user = Contact.query.filter_by(username=username).first()

    if user is None:
        return jsonify({"success": False, "message": "Invalid username or password."}), 401

    if user.password != password:  
        return jsonify({"success": False, "message": "Invalid username or password."}), 401

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
    app.run(host="0.0.0.0", port=5000, debug=True)
