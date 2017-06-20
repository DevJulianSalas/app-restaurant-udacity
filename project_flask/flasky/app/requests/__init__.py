from flask import Blueprint

request_blueprint = Blueprint("requests", __name__)

from . import view