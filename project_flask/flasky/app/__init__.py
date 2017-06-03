### Register blueprints  #####
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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

def create_app(config_environment):
    app = Flask(__name__)
    app.config.from_object(config[config_environment])
    config[config_environment].init_app(app)
    db.init_app(app)
    #Here register blueprints
    from user import user_blueprint 
    app.register_blueprint(user_blueprint)
    print(app)
    return app


