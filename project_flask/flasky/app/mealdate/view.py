# -*- coding: utf-8 -*-


# --*-- installed packages --*--
from . import meal_date_blueprint
from flask_restful import reqparse, abort, Api, Resource
from flask import request, jsonify, make_response
from flask_jwt import jwt_required, current_identity

# --*-- installed packages --*--
from ..helper import API_INDEX
from ..serializer_marsh import meal_date_schema
from ..models import Proposal, Request, User
from .. import db


api = Api(meal_date_blueprint)

class ApiMealDateResource(Resource):

    @jwt_required()    
    def get(self):
        pass

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No input data provided'}), 400)
        data, errors = meal_date_schema.load(json_data)
        if errors:
            return make_response(jsonify({'message': errors}), 422)
        if not data.get("is_accept"):
            return make_response(jsonify("Se va a eliminar"))
        








api.add_resource(ApiMealDateResource, API_INDEX + "mealdate")