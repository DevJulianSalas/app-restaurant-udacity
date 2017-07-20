# -*- coding: utf-8 -*-


# --*-- installed packages --*--
from . import meal_date_blueprint
from flask_restful import reqparse, abort, Api, Resource
from flask import request, jsonify, make_response
from flask_jwt import jwt_required, current_identity

# --*-- installed packages --*--
from ..helper import API_INDEX, get_geo_google_api, find_restaurant_meet
from ..serializer_marsh import (
    meal_date_schema, meal_data_get_schema, update_meal_data,
    meal_data_get_specific
    )
from ..models import Proposal, Request, MealDate
from .. import db


api = Api(meal_date_blueprint)

class ApiMealDatasResource(Resource):

    @jwt_required()    
    def get(self):
        """Return all dates acording to request of user id"""
        meal_dates = MealDate.query.filter(
            MealDate.user_id_proposal== current_identity.id\
            or MealDate.user_id_request == current_identity.id
        ).all()
        data, error = meal_data_get_schema.dump(meal_dates)
        if error:
            print(error)
        return make_response(jsonify(data))

    @jwt_required()
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No input data provided'}), 400)
        data, errors = meal_date_schema.load(json_data)
        if errors:
            return make_response(jsonify({'message': errors}), 422)
        if not data.get("is_accept"):
            return make_response(jsonify("Se va a eliminar"))
        request_info = Request.query.filter(
            Request.id == data.get("id_request", None),
            Request.user_id == current_identity.id).first()
        
        info_location = get_geo_google_api(request_info.location_request)
        find_restaurant = find_restaurant_meet(request_info.meal_type,info_location)
        proposal_users = Proposal.query.filter(
            Proposal.request_id==data.get('id_request',None)).all()
        meal_date = MealDate.insert_meal_date(
            find_restaurant, current_identity, proposal_users,
            request_info
        )
        request_info.filled = True
        request_info.save()
        object_response = {
            "message": "Created User",
            "created": True,
            "id": meal_date.id 
        }
        return make_response(jsonify(object_response))

    @jwt_required()
    def put(self):
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No input data provided'}), 400)
        data, errors = update_meal_data.load(json_data)
        if errors:
            return make_response(jsonify({'message': errors}), 422)
        meal_data = MealDate.update_meal_date(current_identity, data)
        if not meal_data:
            response = {
                "message": "Not is a participant user of this date"
            }
            return make_response(jsonify(response))
        response = {
            "message": "Update user successfull",
            "update": True
        }
        return make_response(jsonify(response))


class ApiMealDataResource(Resource):
    
    @jwt_required()
    def get(self):
        json_data = request.args.to_dict()
        if not json_data:
            return make_response(jsonify({'message': 'No param data provided'}), 400)
        meal_date = MealDate.get_specific_meal_date(
            json_data, current_identity
        )
        if not meal_date:
            response = {
                "message": "There is not proposal with that id"
            }
            return make_response(jsonify(response))
        data, error = meal_data_get_specific.dump(meal_date)
        if error:
            response = {
                "message": "There was a problem, try again"
            }
            return make_response(jsonify(data))
        return make_response(jsonify(data))
        
        
        

api.add_resource(ApiMealDatasResource, API_INDEX + "mealdate")
api.add_resource(ApiMealDataResource, API_INDEX + "mealdate/")