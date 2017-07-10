# -*- coding: utf-8 -*-



# --*-- installed packages --*--
from flask_restful import reqparse, abort, Api, Resource
from flask import request, jsonify, make_response
from flask_jwt import jwt_required, current_identity

# --*-- own packages --*--
from ..helper import API_INDEX
from ..serializer_marsh import request_schema, requests_schema, request_update_schema
from ..models import User, Request
from .. import db
from . import request_blueprint

    
        

api = Api(request_blueprint)

@request_blueprint.route("/requests")
def user():
    return "requests task"


class ApiRequestsResource(Resource):
    """
    Doc Resource
    """
    
    decorators = [jwt_required()]
    
    def get(self):
        """get all register from request"""
        requests = Request.get_all_data(current_identity.id)
        data, errors = requests_schema.dump(requests)
        if errors:
            print(errors)
        return make_response(jsonify(data))

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No input data provided'}), 400)
        data, errors = request_schema.load(json_data)
        if errors:
            return make_response(jsonify({'message': errors}), 422)
        
        user_data = User.query.get(json_data["user_id"])
        if user_data is None:
            return make_response(jsonify(
                {
                    "message": "Id user not found, check out id",
                    "user_id": json_data["user_id"]
                }
            )
        )
        requests = Request(
            meal_type = data["meal_type"], location_request = data["location_request"],
            latitud = data["latitud"], meal_time = data["meal_time"],filled_limit= data["filled"],
            user = user_data
        )
        requests.save()
        result,error = request_schema.dump(Request.query.get(requests.id))
        return make_response(
            jsonify({
                "message": "Created request",
                "id_request": result.get("id",None),
                "user_id": result.get("user_id",None)
                
            })
        )
    
    @jwt_required()
    def put(self):
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No input data provided'}), 400)
        data, errors = request_update_schema.load(json_data)
        if errors:
            return make_response(jsonify({'message': errors}), 422)
        update_request = Request.update_request(current_identity.id, data)
        if not update_request:
            return make_response(jsonify({'message': 'Failed update request, check out params'}), 400)
        response = {
            "message": "Update user successfull",
            "update": True
        }
        return make_response(jsonify(response))
        
        
        


class ApiRequestResource(Resource):
    """
    Manage resource to get a specifyc request
    methods:
        get -> return an unique request
            params: id the request.
    Note:
        get method is necesary token to consume resource
    """
    @jwt_required()
    def get(self):
        json_data = request.args.to_dict()
        if not json_data:
            return make_response(jsonify({'message': 'No input data provided'}), 400)
        specifyc_request =\
                Request.get_specifyc_request(json_data.get("id",None))
        if specifyc_request is None:
            response = {
                "message": "Opps Request could not be found"
            }
            return make_response(jsonify(response), 400)
        response, error = request_schema.dump(specifyc_request)
        return make_response(jsonify(response))
        
    


api.add_resource(ApiRequestsResource, API_INDEX + 'requests')
api.add_resource(ApiRequestResource, API_INDEX + 'requests/')