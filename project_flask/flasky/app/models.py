from . import db
from flask_sqlalchemy import SQLAlchemy



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(120))
    age = db.Column(db.Integer)
    # requests = db.relationship('Request', backref='user',
    #                           lazy='dynamic')
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_type = db.Column(db.String(100), nullable=False)
    location_request = db.Column(db.String(100), nullable=False)
    latitud = db.Column(db.String(100),nullable=False)
    meal_time = db.Column(db.DateTime(), nullable=False)
    filled = db.Column(db.Integer)
    user = db.relationship('User', backref=db.backref("quotes", lazy="dynamic"))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def save(self):
        db.session.add(self)
        db.session.commit()

        
# class Proposal(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_proposed_to = db.Column(db.String(100), nullable=False)
#     user_proposed_from = db.Column(db.String(100), nullable=False)
#     filled = db.Column(db.Integer)
#     request_id = db.relationship(Request, backref='proposal',
#                               lazy='dynamic')

# class MealDate(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     restaurant_name = db.Column(db.String(100), nullable=False)
#     restaurant_address = db.Column(db.String(100), nullable=False)
#     restaurant_picture = db.Column(db.String(100), nullable=False)
#     meal_time = db.Column(db.DateTime(), nullable=False)

