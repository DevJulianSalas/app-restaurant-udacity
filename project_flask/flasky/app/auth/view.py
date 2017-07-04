# -*- coding: utf-8 -*-

# --*-- installed packages --*--
from flask_restful import Api 
from flask import request, jsonify, redirect
from flask_jwt import JWT
# --*-- own packages --*--
from . import auth_blueprint
# from ..serializer_marsh import user_schema
from ..models import User
from .. import bcrypt

api = Api(auth_blueprint)


def authenticate(username, password):
    user = User.query.filter_by(name=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)



        



