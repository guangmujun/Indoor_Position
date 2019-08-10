from indoor_position import db

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.Text)
    city = db.Column(db.Text)
    area = db.Column(db.Text)
    
