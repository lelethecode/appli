from config import db

class Contact3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120),nullable = False,unique = True)
    man = db.Column(db.Integer)
    ngot = db.Column(db.Integer)
    cay = db.Column(db.Integer)
    des = db.Column(db.Text)
    ima = db.Column(db.Text)
    # diung = db.Column(db.Integer,unique = False,nullable = True)
    def to_json(self):
        return{
            "id": self.id,
            "man":self.man,
            "ngot":self.ngot,
            "cay":self.cay,
            "username":self.username,
            "des":self.des,
            "ima":self.ima,
            # "diung":self.diung,
        }
