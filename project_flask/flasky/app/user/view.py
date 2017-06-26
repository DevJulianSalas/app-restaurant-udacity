from . import user_blueprint
from flask_restful import reqparse, abort, Api, Resource
from flask import request, jsonify, make_response
from ..helper import API_INDEX
from ..models import User
from ..serializer_marsh import user_schema
from ..models import User
from .. import db

api = Api(user_blueprint)

@user_blueprint.route("/index")
def index():
    return "Testing blueprints"




class ApiUserResource(Resource):
    
    def post(self):
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
        result = user_schema.dump(User.query.get(user.id))
        return make_response(
            jsonify(
                {
                    "message": "Created User",
                    "User": result.data["name"],
                    "id": result.data["id"]
                }
            )
        )


        
        
    
        

        

        
        
        
        
        


api.add_resource(ApiUserResource, API_INDEX + 'create/user')

