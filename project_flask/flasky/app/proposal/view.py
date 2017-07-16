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
from ..models import Proposal, Request, User
from .. import db


api = Api(proposal_to_request)




class ApiProposalsResource(Resource):

    @jwt_required()
    def get(self):
        proposal = Proposal.get_proposals_by_id(
            current_identity
        )
        
        data, error = proposals_schema.dump(proposal)
        if error:
            response = {
                "Error": "There was a problem try again"
            }
            make_response(jsonify(response), 500)
        return make_response(jsonify(data))

    @jwt_required()
    def post(self):
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No input data provided'}), 400)
        print(json_data)
        data, errors = proposal_schema.load(json_data)
        if errors:
            return make_response(jsonify({'message': errors}), 422)
        check_proposal_exist = Proposal.check_if_proposal_user_exist(data)
        if check_proposal_exist:
            response = {
                "message" : "You should not make a proposal with same id",
                "id": data.get("request_id")
            }
            return make_response(jsonify(response))
        
        user_make_request = Request.query.get(
            data.get("request_id", None)
        )
        user_propo_to_request = User.query.get(
            data.get("user_proposed_from", None)
        )
        user_exist = User.query.get(user_make_request.user_id)
        if user_exist is None or user_propo_to_request is None:
            response = {
                "message": "Error not exist, checkout if users exist"
            }
            return make_response(jsonify(response))
        proposal = Proposal(
            request_id=user_make_request.id,
            user_proposed_to=user_make_request.user_id,
            user_proposed_from=data.get("user_proposed_from",None)
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
    
    @jwt_required()
    def put(self):
        json_data = request.get_json()
        if not json_data:
            return make_response(jsonify({'message': 'No input data provided'}), 400)
        data, errors = proposal_update_schema.load(json_data)
        if errors:
            return make_response(jsonify({'message': errors}), 422)
        proposal = Proposal.update_proposal(current_identity, data)
        if not proposal:
            return make_response(jsonify({'message': 'There was a problem, try again'}), 500)
        response = {
            "message": "Update user successfull",
            "update": True
        }
        return make_response(jsonify(response))
        

    

class ApiProposalResource(Resource):
    @jwt_required()
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
        

        
        



api.add_resource(ApiProposalsResource, API_INDEX + "proposal")
api.add_resource(ApiProposalResource, API_INDEX + "proposal/<int>:id")