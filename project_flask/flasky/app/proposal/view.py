from . import proposal_to_request
from flask_restful import reqparse, abort, Api, Resource
from flask import request, jsonify, make_response
from ..helper import API_INDEX
from ..serializer_marsh import proposal_schema
from ..models import Proposal, Request
from .. import db


api = Api(proposal_to_request)

@proposal_to_request.route("/proporsal")
def proporsal():
    return "Proporsal"


class ApiProposalResource(Resource):

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No input data provided'}), 400)
        data, errors = proposal_schema.load(json_data)
        if errors:
            return make_response(jsonify({'message': errors}), 422)
        user_id_request = Request.query.get(data.get("request_id", None))
        if user_id_request is None:
            return make_response(
                jsonify({'message': 'There was a problem with request_id',}), 400)
        proposal = Proposal(
            request_id=user_id_request.id,
            user_proposed_to=data.get("user_proposed_to",None),
            user_proposed_from=user_id_request.user_id
        )
        proposal.save()
        result, error = proposal_schema.dump(Proposal.query.get(proposal.id))
        return make_response(
            jsonify(
                {
                    "message":"Create proposal",
                    "id_proposal": result.get("id",None)
                }
            )
        )
            
        
        
        

        
        



api.add_resource(ApiProposalResource, API_INDEX + "create/proposal")