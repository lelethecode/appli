from config import db

class Contact2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120),nullable = False,unique = True)
    check = db.Column(db.Boolean, default=False)
    man = db.Column(db.Integer)
    ngot = db.Column(db.Integer)
    cay = db.Column(db.Integer)
    # diung = db.Column(db.Integer,unique = False,nullable = True)
    def to_json(self):
        return{
            "id": self.id,
            "man":self.man,
            "ngot":self.ngot,
            "cay":self.cay,
            "username":self.username,
            "check":self.check,
            # "diung":self.diung,
        }
