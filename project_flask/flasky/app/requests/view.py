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
        user_data = User.query.get(json_data["user_id"])
        if user_data is None:
            return make_response(jsonify(
                {"message": "User not found with that id, check out it",
                 "info": json_data["user_id"]}
            ))
        json_data["user_id"] =user_data
        data, errors = request_schema.load(json_data)
        if errors:
            return make_response(jsonify({'message': errors}), 422)
        requests = Request(
            meal_type = data["meal_type"], location_request = data["location_request"],
            latitud = data["latitud"], meal_time = data["meal_time"],filled= data["filled"],
            user = user_data
        )
        requests.save()
        result = request_schema.dump(Request.query.get(requests.id))
        print(result)
        return make_response(
            jsonify({
                "message": "Created request",
                "id_request": result[0]["id"],
                "user": result[0]["user"]["name"]
                
            })
        )

api.add_resource(ApiRequestsResource, API_INDEX + 'create/request')