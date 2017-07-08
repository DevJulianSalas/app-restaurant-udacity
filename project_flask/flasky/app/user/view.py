

# --*-- installed packages --*--
from . import user_blueprint
from flask_restful import reqparse, abort, Api, Resource
from flask import request, jsonify, redirect, make_response
from flask_jwt import jwt_required, current_identity


# --*-- own packages --*--
from ..helper import API_INDEX
from ..models import User
from ..serializer_marsh import user_result_schema, users_result_schema, update_user_result_schema
from ..models import User
from .. import db


api = Api(user_blueprint)

    
class ApiUsersResource(Resource):
    """
    Manage the path resources to User
    methods:
        get  -> return all users 
        post -> create an user 
        put  -> update an user
        delete -> delete an user
    Note:
        the get, put, delete methods ask them jwt token to 
        authorizate access
    
    """
    
    @jwt_required()
    def get(self):
        """Return profile information about all users system"""
        users = User.query.all()
        result, error = users_result_schema.dump(users)
        if error:
            print(error)
        return make_response(jsonify(result))

    
    def post(self):
        """return token and create user if isn't by oauth provider"""
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No input data provided'}), 400)
        data, errors = user_result_schema.load(json_data)
        if errors:
            return make_response(jsonify({'message': errors}), 422)
        verify_user_exist = User.verify_if_user_exist(data.get("name",None))
        if verify_user_exist:
            response = {
                'message': 'username already exists',
                "created": False
            }
            return make_response(jsonify(response))
        user = User(
            name=data.get("name",None), 
            email=data.get("email",None),
            password_hash=data.get("password_hash",None), 
            age=data.get("age",None)
        )
        user.save()
        object_response = {
            "message": "Created User",
            "created": True,
            "id": user.id 
        }
        return make_response(jsonify(object_response))

    @jwt_required()
    def put(self):
        """Update profile of user with information required"""
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No input data provided'}), 400)
        data, errors = update_user_result_schema.load(json_data)
        if errors:
            return make_response(jsonify({'message': errors}), 422)
        user = User.update_instance_of_user(current_identity.id, data)
        if not user:
            return make_response(jsonify({'message': 'There was a problem, try again'}), 500)
        response = {
            "message": "Update user successfull",
            "update": True
        }
        return make_response(jsonify(response))
            
        

class ApiUserResource(Resource):
    """
    Manage resource to only User
    methods:
        get -> return an unique user
            params: id the user.
    Note:
        get method is necesary token to consume resource
    """
    @jwt_required()
    def get(self):
        json_data = request.args.to_dict()
        if not json_data:
            return make_response(jsonify({'message': 'No input data provided'}), 400)
        try:
            user = User.query.get(json_data.get("id",None))
        except Exception as e:
            response = {
                "message": "Opps User could not be found"
            }
            return make_response(jsonify(response), 400)
        response, error = user_result_schema.dump(user)
        return make_response(jsonify(response))
        

        
    
        


        


        
        
api.add_resource(ApiUsersResource, API_INDEX + 'users')
api.add_resource(ApiUserResource, API_INDEX + 'users/')

