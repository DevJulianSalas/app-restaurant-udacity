from marshmallow import ValidationError

API_INDEX = "/api/v1/"


def must_not_be_blank(data):
    if not data:
        raise ValidationError("data not provided")