### Register blueprints  #####
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_marshmallow import Marshmallow


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

def create_app(config_environment):
    app = Flask(__name__)
    app.config.from_object(config[config_environment])
    config[config_environment].init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    #Here register blueprints
    ma.init_app(app)
    from .user import user_blueprint 
    from .requests import request_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(request_blueprint)
    return app





#######################################

