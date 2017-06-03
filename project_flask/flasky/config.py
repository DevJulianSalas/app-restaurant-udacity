"""General configuration to diferents environments"""
# -*- encoding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

import os



# Root dir

base_dir = os.path.abspath(os.path.dirname(__file__))



class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or "None"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    Debug = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI") or "None"


class TestingConfig(Config):
    Testing = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TESTING_DATABASE_URI") or "None"

class ProductionConfig(Config):
    Testing = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TESTING_DATABASE_URI") or "None"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}