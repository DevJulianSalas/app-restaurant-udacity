from . import db
from flask_sqlalchemy import declarative_base




Base = declarative_base()

class BaseModel(Base):
    """This class content all methods commons to use in differents models"""
    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True)
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model, BaseModel):
    __tablename__ = 'user'
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(120))
    age = db.Column(db.Integer)

    #Relathionship
    user = db.relationship('Request', backref="user", lazy='dynamic')
            

class Request(db.Model, BaseModel):
    __tablename__ = 'request'
    #Foreingkey
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    #Fields
    meal_type = db.Column(db.String(100), nullable=False)
    location_request = db.Column(db.String(100), nullable=False)
    latitud = db.Column(db.String(100),nullable=False)
    meal_time = db.Column(db.DateTime(), nullable=False)
    filled = db.Column(db.Boolean, unique=False, default=False)
    filled_limit = db.Column(db.Integer, default=0)
    
    #Relathionship
    proposal = db.relationship('Proposal', backref="proposal", lazy='dynamic')
    
    
    
    
    
    

        
class Proposal(db.Model, BaseModel):
    __tablename__ = 'proposal'
    
    #ForeignKey
    request_id = db.Column(db.Integer, db.ForeignKey("request.id"))
    #fields
    user_proposed_to = db.Column(db.Integer)
    user_proposed_from = db.Column(db.Integer)
    
    
class MealDate(db.Model, BaseModel):
    __tablename__ = 'mealdate'
    user_id_request = db.Column(db.Integer)
    users_ids = db.Column(db.Integer)
    restaurant_name = db.Column(db.String(100), nullable=False)
    restaurant_address = db.Column(db.String(100), nullable=False)
    restaurant_picture = db.Column(db.String(100), nullable=False)
    meal_time = db.Column(db.DateTime(), nullable=False)

