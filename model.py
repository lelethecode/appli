from config import db

class Contact(db.Model):
    __tablename__ = 'contact' 
    id = db.Column(db.Integer, primary_key=True)
    check = db.Column(db.Integer)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
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
    feedback = db.Column(db.Text)
    def to_json(self):
        return{
            "id": self.id,
            "username": self.username,
            "email":self.email,
            "man":self.man,
            "ngot":self.ngot,
            "password":self.password,
            "cay": self.cay,
            #"A":self.A,
            "favorite_food":self.favorite_food,
            "favorite_food_t2":self.favorite_food_t2,
            "favorite_food_t3":self.favorite_food_t3,
            "favorite_food_t4":self.favorite_food_t4,
            "favorite_food_t5":self.favorite_food_t5,
            "favorite_food_t6":self.favorite_food_t6,
            "check":self.check,
            "feedback": self.feedback
            # "diung":self.diung,
}