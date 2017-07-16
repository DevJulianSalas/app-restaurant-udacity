from flask import Blueprint

meal_date_blueprint = Blueprint("mealdate", '__name__')

from . import view
