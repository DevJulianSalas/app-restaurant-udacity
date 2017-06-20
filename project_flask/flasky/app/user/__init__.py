#Register blueprints by module

from flask import Blueprint

user_blueprint = Blueprint("user", __name__)

from . import view


    