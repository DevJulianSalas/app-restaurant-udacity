
# --*-- Installed packages --*--
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt import JWT

# --*-- Own packages --*--
from config import config





"""
Factory function to get severals instances of this app later.
Use it to test
to run differents settings (developtment,stagin,production).
Remember with factory you can multiples instances of the same
application running in the same aplicaciont process...
"""


# it create object sqlalchemy but not

db = SQLAlchemy()
ma = Marshmallow()
bcrypt =  Bcrypt()


def create_app(config_environment):
    app = Flask(__name__)
    app.config.from_object(config[config_environment])
    config[config_environment].init_app(app)
    #Register plugins to app init
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    #register jwt
    from .auth.view import authenticate, identity

    jwt = JWT(app, authenticate, identity)


    
    #Here register blueprints
    from .user import user_blueprint 
    from .requests import request_blueprint
    from .proposal import proposal_to_request
    from .mealdate import meal_date_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(request_blueprint)
    app.register_blueprint(proposal_to_request)
    app.register_blueprint(meal_date_blueprint)
    # app.register_blueprint(auth_blueprint)
    return app





#######################################

