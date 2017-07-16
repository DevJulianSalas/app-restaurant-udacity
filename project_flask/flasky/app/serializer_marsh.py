from marshmallow import Schema, fields, ValidationError, pre_load, post_load
from .helper import must_not_be_blank
from .models import User, Request
from . import ma, bcrypt
import os



class ValidateTokenSchema(ma.Schema):
    pass





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
    
    @pre_load
    def generate_bycrip_pass(self, data):
        data["password_hash"] = bcrypt.generate_password_hash(
            data["password_hash"], 
            int(os.environ.get('BCRYPT_LOG_ROUNDS'))
        ).decode()
        return data


class UserResultSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=must_not_be_blank)
    email = fields.Email(required=True, validate=must_not_be_blank)
    age = fields.Int(required=True, validate=must_not_be_blank)



class UpdateUserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(validate=must_not_be_blank)
    email = fields.Email(validate=must_not_be_blank)
    password_hash = fields.Str(validate=must_not_be_blank)
    age = fields.Int(validate=must_not_be_blank)
    






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


class RequestUpdateSchema(Schema):
    id = fields.Int(required=True, error_messages= {
        "required": "Id is necesary to update request"
        }
    )
    meal_type = fields.Str(validate = must_not_be_blank)
    location_request = fields.Str(validate=must_not_be_blank)
    meal_time = fields.DateTime(validate=must_not_be_blank)
    filled = fields.Int(validate=must_not_be_blank)
    user_id = fields.Int(validate=must_not_be_blank)





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


class UpdateProposalSchema(Schema):
    id = fields.Int(required=True, error_messages= {
        "required": "Id is necesary to update request"
        }
    )
    user_proposed_to = fields.Int(
        error_messages = {"required": "id user is required to register proposal"},
        validate=must_not_be_blank
    )
    user_proposed_from = fields.Int(
        error_messages = {"required": "id user is required to reggister proposal"},
        validate=must_not_be_blank
    )






#User    
user_result_schema = UserSchema(only=('name', 'email'))
users_result_schema = UserResultSchema(only=('name', 'email'),many=True)
update_user_result_schema = UpdateUserSchema()


#Request
request_schema = RequestsSchema()
requests_schema = RequestsSchema(many=True)
request_update_schema = RequestUpdateSchema()

#proposal
proposal_schema = ProposalSchema()
proposals_schema = ProposalSchema(many=True)
proposal_update_schema = UpdateProposalSchema()
