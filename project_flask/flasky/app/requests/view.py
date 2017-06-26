from . import request_blueprint
from flask_restful import reqparse, abort, Api, Resource
from flask import request, jsonify, make_response
from ..helper import API_INDEX
from ..serializer_marsh import request_schema, user_schema, requests_schema
from ..models import User, Request
from .. import db

    
        

api = Api(request_blueprint)

@request_blueprint.route("/requests")
def user():
    return "requests task"


class ApiRequestsResource(Resource):

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

api.add_resource(ApiRequestsResource, API_INDEX + 'create/request')