
from . import db
from flask_sqlalchemy import declarative_base
import os
from datetime import datetime, timedelta


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
    active = db.Column(db.Boolean, default=False)
    age = db.Column(db.Integer)
    token = db.Column(db.Text)


    def encode_auth_token(self, user_id):
        """
        generate auth token
        """
        try:
            payload = {
                'exp': datetime.now() + timedelta(days=0, seconds=59),
                'iat': datetime.now(),
                'sub': user_id
                }
            return jwt.encode(payload, os.environ.get('SECRET_KEY'), 
                algorithm='HS256'
            )
        except Exception as e:
            raise e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        decode auth token
        :return str or int
        """
        try:
            payload = jwt.decode(auth_token, os.environ.get('SECRET_KEY'))
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
    
    @staticmethod
    def verify_if_user_exist(user_name):
        """
        return true if user exist
        params: user_name str username
        return Bool
        """
        result_query_user = User.query.filter_by(name=user_name).first()
        if result_query_user:
            return True
    
    @staticmethod
    def update_instance_of_user(id, data):
        """
        return instance of user updated if there is one user.
        params: data => something value to search in columns to return data
        """
        try:
            user_update = User.query.filter_by(id=id).update(data)
        except Exception as e:
            print(e)
            return False
        if user_update:
            db.session.commit()
            return user_update
        
        
        
    
    
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
    


    @staticmethod
    def get_all_data(user_id):
        """Return all request from Request except the requests of own user_id"""
        try:
            list_request = list()
            for data in Request.query.filter(Request.user_id != user_id):
                list_request.append(data)
            return list_request
        except Exception as error:
            print(error)
            db.session.rollback()

    @staticmethod
    def get_specifyc_request(id_request):
        try:
            result_request = Request.query.get(id_request)
            return result_request
        except Exception as error:
            print(error)
            db.session.rollback()

    @staticmethod
    def update_request(user_id, data_update):
        try:
            request_update = Request.query.filter(\
                Request.user_id == user_id, 
                Request.id == data_update.get("id", None)
                ).update(data_update)
        except Exception as e:
            print(e)
            return False
        if request_update:
            db.session.commit()
            return request_update
        else:
            return False
        
        
        
        
    
    
    
    
    

        
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

