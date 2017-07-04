

# --*-- installed packages --*--
from . import user_blueprint
from flask_restful import reqparse, abort, Api, Resource
from flask import request, jsonify, redirect, make_response
from flask_jwt import jwt_required


# --*-- own packages --*--
from ..helper import API_INDEX
from ..models import User
from ..serializer_marsh import user_schema, user_result_schema
from ..models import User
from .. import db


api = Api(user_blueprint)

    
class ApiUserResource(Resource):
    
    @jwt_required()
    def get(self):
        """Return profile information about all users system"""
        users = User.query.all()
        result, error = user_result_schema.dump(users)
        if error:
            print(error)
        return make_response(jsonify(result))

    
    def post(self):
        """return token and create user if isn't by oauth provider"""
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No input data provided'}), 400)
        data, errors = user_schema.load(json_data)
        if errors:
            return make_response(jsonify({'message': errors}), 422)
        user = User(
            name=data.get("name",None), 
            email=data.get("email",None),
            password_hash=data.get("password_hash",None), 
            age=data.get("age",None)
        )
        user.save()
        object_response = {
            "message": "Created User",
            "id": user.id 
        }
        return make_response(jsonify(object_response))


        
        
api.add_resource(ApiUserResource, API_INDEX + 'users')

