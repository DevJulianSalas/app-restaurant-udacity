from flask import Blueprint

proposal_to_request = Blueprint("proposal", '__name__')

from . import view
