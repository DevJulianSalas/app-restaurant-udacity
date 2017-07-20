from marshmallow import (
    Schema, fields, ValidationError, pre_load, post_load,
    validates

    )
from .helper import must_not_be_blank
from .models import User, Request
from . import ma, bcrypt
import os

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
        if data.get("password_hash"):
            data["password_hash"] = bcrypt.generate_password_hash(
                data.get("password_hash"), 
                int(os.environ.get('BCRYPT_LOG_ROUNDS'))
            ).decode('utf-8')
            return data
        else:
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

    @pre_load
    def generate_bycrip_pass(self, data):
        if data.get("password_hash"):
            data["password_hash"] = bcrypt.generate_password_hash(
                data.get("password_hash"), 
                int(os.environ.get('BCRYPT_LOG_ROUNDS'))
            ).decode('utf-8')
            return data
        else:
            return data
    
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

    @pre_load
    def valitade_ids_users_same(self, data):
        if data.get("user_proposed_to") == data.get("user_proposed_from"):
            raise ValidationError("user_from should not same to user_to")
            return data
        return data
        
        


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

class MealDateSchema(Schema):
    is_accept = fields.Boolean(
        required = True, error_messages={
            "required": "Accept field is required"
        }
    )
    id_request = fields.Int(
        required = True,
        error_messages = {"required": "id request is required to acept mealdate"},
        validate=must_not_be_blank
    )

    
class MealDateGetSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id_request = fields.Int(required = True)
    user_id_proposal = fields.Int(required = True)
    restaurant_name = fields.Str(required = True)
    restaurant_address = fields.Str(required = True)
    restaurant_picture = fields.Str(required = True)
    meal_time = fields.DateTime(required = True)

    
class UpdateMealDateGetSchema(Schema):
    id = fields.Int(required=True, error_messages= {
        "required": "Id is necesary to update request"
        }
    )
    user_id_request = fields.Int(validate=must_not_be_blank)
    user_id_proposal = fields.Int(validate=must_not_be_blank)
    restaurant_name = fields.Str(validate=must_not_be_blank)
    restaurant_address = fields.Str(validate=must_not_be_blank)
    restaurant_picture = fields.Str(validate=must_not_be_blank)
    meal_time = fields.DateTime(validate=must_not_be_blank)



#User    
user_result_schema = UserSchema()
get_only_user_schema = UserSchema(only=("name", "email"))
users_result_schema = UserResultSchema(only=('name', 'email'),many=True)
update_user_result_schema = UpdateUserSchema()
delete_user_result_schema = UserSchema(only=("id"))



#Request
request_schema = RequestsSchema()
requests_schema = RequestsSchema(many=True)
request_update_schema = RequestUpdateSchema()

#proposal
proposal_schema = ProposalSchema()
proposals_schema = ProposalSchema(many=True)
proposal_update_schema = UpdateProposalSchema()



#mealdate
meal_date_schema = MealDateSchema()
meal_data_get_schema = MealDateGetSchema(many=True)
meal_data_get_specific = MealDateGetSchema()
update_meal_data = UpdateMealDateGetSchema()