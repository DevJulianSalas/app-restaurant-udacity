"""General configuration to diferents environments"""
# -*- encoding: utf-8 -*-

# --*-- insatalled packages --*--
from flask_sqlalchemy import SQLAlchemy
import os

# --*-- built-in packages --*--
from datetime import timedelta




# Root dir

base_dir = os.path.abspath(os.path.dirname(__file__))




class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or "None"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    JWT_EXPIRATION_DELTA = timedelta(days=30)
    
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI") or "None"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TESTING_DATABASE_URI") or "None"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("None") or "None"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}