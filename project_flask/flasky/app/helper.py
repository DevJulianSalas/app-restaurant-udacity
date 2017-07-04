

# --*-- installed packages --*--
from marshmallow import ValidationError
from requests_oauthlib import OAuth2Session



# --*-- own packages --*--
from .models import User
from . import bcrypt



API_INDEX = "/api/v1/"


def must_not_be_blank(data):
    if not data:
        raise ValidationError("data not provided")


# def get_googl_auth(state=None, token=None):
#     """return oauth object"""
#     if token:
#         return OAuth2Session(Auth.CLIENT_ID, token = token)
#     if state:
#         return OAuth2Session(
#             Auth.CLIENT_ID,
#             state = state,
#             redirect_uri = Auth.REDIRECT_URI
#         )
#     outah = OAuth2Session(
#         Auth.CLIENT_ID,
#         redirect_uri = Auth.REDIRECT_URI,
#         scope = Auth.SCOPE
#     )
