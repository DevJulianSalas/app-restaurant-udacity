from marshmallow import Schema, fields, ValidationError, pre_load, post_load
from .helper import must_not_be_blank
from .models import User, Request
from . import ma

class UserSchema(ma.Schema):
    # class Meta:
    #     model = User
        # fields = ('id', 'name','email','password_hash','age')
    
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=must_not_be_blank)
    email = fields.Email(required=True, validate=must_not_be_blank)
    password_hash = fields.Str(required=True, validate=must_not_be_blank)
    age = fields.Int(required=True, validate=must_not_be_blank)

    def format_name(self, user):
        return "{}, {}".format(user.name, user.email)
    

    # class Meta:
    #     fields = "__all__"
class RequestsSchema(Schema):

    id = fields.Int(dump_only=True)
    meal_type = fields.Str(
        required=True, 
        error_messages = {"required": "meal_type is required."},
        validate = must_not_be_blank
    )
    location_request = fields.Str(required=True, validate=must_not_be_blank)
    latitud = fields.Str(required=True, validate=must_not_be_blank)
    meal_time = fields.DateTime(required=True, validate=must_not_be_blank)
    filled = fields.Int(required=True, validate=must_not_be_blank)
    user_id = fields.Int(
        required=True,
        error_messages = {"required": "id user is required to request object"},
        validate=must_not_be_blank)

class ProposalSchema(Schema):
    id = fields.Int(dump_only=True)
    request_id = fields.Int(
        required=True,
        error_messages = {"required": "id request is required to register proposal"},
        validate=must_not_be_blank
    )
    user_proposed_to = fields.Int(
        required=True,
        error_messages = {"required": "id user is required to register proposal"},
        validate=must_not_be_blank
    )
    user_proposed_from = fields.Int(
        required=True,
        error_messages = {"required": "id user is required to reggister proposal"},
        validate=must_not_be_blank
    )


    
user_schema = UserSchema()
users_schema = UserSchema(many=True)

request_schema = RequestsSchema()
requests_schema = RequestsSchema(many=True)

proposal_schema = ProposalSchema()
proposals_schema = ProposalSchema(many=True)
