# -*- coding: utf-8 -*-

# --*-- built-in packages --*--
import os
from datetime import datetime, timedelta

# --*-- own packages --*--
from . import db

# --*-- Installed packages --*--
from flask_sqlalchemy import declarative_base
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError


Base = declarative_base()

class BaseModel(Base):
    """This class content all methods commons to use in differents models"""
    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True)
    # create_on = db.Column(DateTime(),)
    # update_on = db.Column(DateTime(),)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
class User(db.Model, BaseModel):
    __tablename__ = 'user'
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    user_name = db.Column(db.String(120), unique = True)
    password_hash = db.Column(db.String(120))
    active = db.Column(db.Boolean, default=False)
    age = db.Column(db.Integer)
    
    #Relathionship
    user = db.relationship('Request', backref="user", lazy='dynamic')


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
        Search by user_name exist.
            params: user_name str username
            return object found in mapper
        """
        is_user = None
        try:
            is_user = User.query.filter_by(
                user_name=user_name).first()
        except SQLAlchemyError as error:
            print(error) #here make a loggin data to track!
            db.session.rollback()
            return None
        else:
            if is_user:
                return is_user
            else:
                return False
            
    
    @staticmethod
    def update_instance_of_user(id, data):
        """
        update user according to data passed
            params: data => is a dict of data to update
            return instance of user updated if there is one user 
            or None if there is no user.
        """
        user_update = None
        try:
            user_update = User.query.filter_by(id=id).update(data)
        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
        else:
            db.session.commit()
            return user_update
        
    # @staticmethod
    # def delete_user(identify):
    #     result_query = None
    #     try:
    #         result_query = User.query.get(identify.id)
    #     except Exception as e:
    #         return result_query
    #     return result_query
        
        
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
        """
        Search by all requests distinct of themselves 
            params: user_id is a identify user with id 
            Return all requests except the requests of user_id
        """
        list_requests = list()
        try:
            for data in Request.query.filter(Request.user_id != user_id.id):
                list_request.append(data)
        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
        else:
            return list_requests

    @staticmethod
    def get_specifyc_request(id_request):
        """
        Get specific request with id request
            params: id of request
            return request instance-
        """
        result_request = None
        try:
            result_request = Request.query.get(id_request)
        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
        else:
            return result_request

    @staticmethod
    def update_request(user_id, data_update):
        """
        Update request, only user who made request, can update request
            params: user_id is a indentify to know if user exist
                    data_update is a dict to update information about
                        request
            return flag if or not update request
        """
        request_update = False
        try:
            request_update = Request.query.filter(
                                Request.user_id == user_id.id, 
                                Request.id == data_update.get("id", None)
                                ).update(data_update)
        except SQLAlchemyError as error:
            print(e)
            db.session.rollback()
        else:
            db.session.commit()
            return request_update
                        
class Proposal(db.Model, BaseModel):
    __tablename__ = 'proposal'
    
    #ForeignKey
    request_id = db.Column(db.Integer, db.ForeignKey("request.id"))
    #fields
    user_proposed_to = db.Column(db.Integer) #user makes request
    user_proposed_from = db.Column(db.Integer) # user make proposal to user makes request

    @staticmethod
    def check_if_proposal_user_exist(data):
        """
        Check if an user already made proposal with that request_id or.
            params: data is a dict with request_id and user_proposed_from
            return None if user not is found or 
        
        """
        user_proposal = None
        try:
            user_proposal = Proposal.query.filter(
                Proposal.request_id == data.get("request_id"),
                Proposal.user_proposed_from == data.get("user_proposed_from")
            ).count()
        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
        else:
            return user_proposal
    
    @staticmethod
    def get_proposals_by_id(currenty_user):
        """
        Get proposals according to id.
            params: currenty_user is an identification user.
            return: a list of proposal instances.

        """
        list_proposals = list()
        try:
            for proposal in Proposal.query.filter(Proposal.user_proposed_to==\
                                                  currenty_user.id):
                list_proposals.append(proposal)
        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
        else:
            return list_proposals

    @staticmethod
    def get_specific_proposal(id_proposal, info_user):
        """
        get specific proposal if user and id proposal exist.
            params: id_proposal is an id of proposal registry.
                    info_user is an id of user who want get proposal
            return: instance of proposal.
        """
        proposal = None
        try:
            proposal = Proposal.query.filter(
                Proposal.id == id_proposal,
                Proposal.user_proposed_from == info.get("id", None) or\
                Proposal.user_proposed_to == info_user.get("id")
            )
        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
        else:
            return proposal

    @staticmethod
    def update_proposal(current_user, data_update):
        """
        update information of a proposal if current user exist 
        in proposals the request.
            params: current_user

        """
        try:
            exist_user_proposal = Proposal.query.filter(
                Proposal.user_proposed_from == current_user.id
            )
        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
        else:
            return False
        try:
            update_proposal = Proposal.query.filter_by(
                id=data_update.get('id', None)).update(data_update)
        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
        else:
            if update_proposal:
                db.session.commit()
                return update_proposal
            
class MealDate(db.Model, BaseModel):
    __tablename__ = 'mealdate'
    user_id_request = db.Column(db.Integer)
    user_id_proposal = db.Column(db.Integer)
    restaurant_name = db.Column(db.String(100), nullable=False)
    restaurant_address = db.Column(db.String(100), nullable=False)
    restaurant_picture = db.Column(db.String(100), nullable=False)
    meal_time = db.Column(db.DateTime(), nullable=False)

    @staticmethod
    def insert_meal_date(meal_date_info, current_id, 
        user_id_proposals, request_info):
        """
        Insert meald date of 1 or mor users proposal.
            params: meald_date_info str 
                    current_id int is id of current user
                    request_info is a date of a made request
                    user_id_proposals, update info for all users
            return: true if update or false if not.
        """
        if len(user_id_proposals) > 0:
            meal_date = None
            try:
                for user_proposal in user_id_proposals:
                    meal_date = MealDate(
                        user_id_request = current_id.id,
                        user_id_proposal = user_proposal.id,
                        restaurant_name = meal_date_info.get("name", None),
                        restaurant_address = meal_date_info.get("address", None),
                        restaurant_picture = meal_date_info.get("image", None),
                        meal_time = request_info.meal_time
                    )
                    db.session.add(meal_date)
            except SQLAlchemyError as error:
                print(errror)
                db.session.rollback()
            else:
                db.session.commit()
                return meal_date

    @staticmethod
    def update_meal_date(current_data, data_update):
        """
        Update meal date if current id exist.
            params: current_data is a current object user 
                    data_update is a dict with information
                        about meal to update.
            return: 
        """
        is_meal_date = None
        try:
             is_meal_date = MealDate.query.filter(
                        MealDate.user_id_request == current_data.id\
                        or MealDate.user_id_proposal == current_data.id
                        )
        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
        else:
            if not is_meal_date:
                return False
        try:
            update_meal_date = MealDate.query.filter_by(
                    id = data_update.get('id', None)).update(data_update)
        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
        else:
            if update_meal_date:
                db.session.commit()
                return update_meal_date

    @staticmethod
    def get_specific_meal_date(id_meal_date, current_identity):
        """
        get specific meal date for current id user
            params: id_meal_date int is an id of meal date to search
                    current_identity, is a current object user
        """
        specific_meal_date = None
        try:
            specific_meal_date = MealDate.query.filter(
                    MealDate.id == id_meal_date.get("id", None))\
                    .filter(
                            or_(MealDate.user_id_request  == current_identity.id,
                            MealDate.user_id_proposal == current_identity.id
                            )
                    ).first()
        except SQLAlchemyError as error:
            print(error)
            db.session.rollback()
        else:
            return specific_meal_date
        

        
            
            

    
    

