#Register blueprints by module
from flask import Blueprint

auth_blueprint = Blueprint("auth", __name__)

from . import view
