# -*- encoding: utf-8 -*-

# --*-- built-in packages --*--
import os

# --*-- install packages --*--
from flask import Flask
from flask_script import Manager, Shell, Server, prompt_bool
from flask_migrate import Migrate, MigrateCommand

# --*-- own packages --*--
from app import create_app, db




app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

from app import models

manager.add_command('db', MigrateCommand)


#methods to manage flask app

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, models=models)

@manager.command
def dropdb():
    if prompt_bool("Are you sure want to lose all your data"):
        print("test delete db")
        #db.drop_all()

        






if __name__ == '__main__':
    manager.run()