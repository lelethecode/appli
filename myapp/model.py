from config import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check = db.Column(db.Integer)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    man = db.Column(db.Integer)
    ngot = db.Column(db.Integer)
    cay = db.Column(db.Integer)
    A = db.Column(db.String(120))
    favorite_food = db.Column(db.String(120))
    # diung = db.Column(db.Integer,unique = False,nullable = True)
    def to_json(self):
        return{
            "id": self.id,
            "username": self.username,
            "email":self.email,
            "man":self.man,
            "ngot":self.ngot,
            "password":self.password,
            "cay": self.cay,
            "A":self.A,
            "favorite_food":self.favorite_food,
            "check":self.check
            # "diung":self.diung,
        }