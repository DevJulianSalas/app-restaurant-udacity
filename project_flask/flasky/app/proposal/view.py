# -*- coding: utf-8 -*-


# --*-- installed packages --*--
from . import proposal_to_request
from flask_restful import reqparse, abort, Api, Resource
from flask import request, jsonify, make_response
from flask_jwt import jwt_required, current_identity

# --*-- installed packages --*--
from ..helper import API_INDEX
from ..serializer_marsh import (
    proposal_schema, proposals_schema, proposal_update_schema
)
from ..models import Proposal, Request
from .. import db


api = Api(proposal_to_request)

@proposal_to_request.route("/proporsal")
def proporsal():
    return "Proporsal"


class ApiProposalsResource(Resource):

    @jwt_required
    def get(self):
        proposal = Proposal.get_proposal_by_id(
            current_identity
        )
        data, error = proposals_schema.dump(proporsal)
        if error:
            response = {
                "Error": "There was a problem try again"
            }
            make_response(jsonify(response), 500)
        return make_response(jsonify(data))

    @jwt_required
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
        if user_id_request.user_id == data.get("user_proposed_to",None):
            response = {
                "info": "User request is the same of proposal not allowed"
            }
            return make_response(jsonify(response))
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
    
    @jwt_required
    def put(self):
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No input data provided'}), 400)
        data, errors = proposal_update_schema.load(json_data)
        if errors:
            return make_response(jsonify({'message': errors}), 422)
        proposal = Proposal.update_proposal(current_identity.id, data)
        if not proposal:
            return make_response(jsonify({'message': 'There was a problem, try again'}), 500)
        response = {
            "message": "Update user successfull",
            "update": True
        }
        return make_response(jsonify(response))
        

    

class ApiProposalResource(Resource):
    @jwt_required
    def get(self):
        json_data = request.args.to_dict()
        if not json_data:
            return make_response(jsonify({'message': 'No param data provided'}), 400)
        proposal = Proposal.get_specific_proposal(
            json_data,current_identity
        )
        if not proporsal:
            response = {
                "message": "There is not proposal with that id"
            }
            return make_response(jsonify(response))
        data, error = proposal_schema.dump(proporsal)
        if error:
            response = {
                "message": "There was a problem, try again"
            }
            return make_response(jsonify(response))
        return make_response(jsonify(data))
        

        
        



api.add_resource(ApiProposalsResource, API_INDEX + "create/proposal")