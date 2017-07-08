import unittest, json
from . import db, create_app
import os
from app.models import User, Request, Proposal
from sqlalchemy import func
from datetime import datetime
import requests
from .helper import API_INDEX
from flask import current_app



class TestDevelopmentConfig(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app(os.getenv('FLASK_CONFIG', default=None))
        self.app_client = self.app.test_client()

    
    def test_app_is_developmnet(self):
        self.assertTrue(self.app.config["DEBUG"] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            self.app.config["SQLALCHEMY_DATABASE_URI"] == 'postgresql://julian_develop:qwerty123@db:5432/desarrollo'
        )







class TestApplication(unittest.TestCase):
    
    def setUp(self):
        #Here call environment testing setting.
        self.app = create_app(os.getenv('FLASK_CONFIG_TESTING', default=None))
        self.user_registry  = None
        self.app_client = self.app.test_client()

        
        
    def tearDown(self):
        """
        Here drop data to ensure that the db is emptied fo next test.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        
    def test_add_user(self):
        with self.app.app_context():
            self.test_user = User(
                name="Julian", 
                email="Juliansalas080@gmail.com",
                password_hash="1qwfsdafas",
                age=27
            )
            db.session.add(self.test_user)
            db.session.commit()
            self.user_registry = self.test_user.query.all()
            self.assertEqual(len(self.user_registry), 1)

    def test_request_user(self):
        with self.app.app_context():
            
            self.test_user = User(
                name="Julian", 
                email="Juliansalas080@gmail.com",
                password_hash="1qwfsdafas",
                age=27
            )
            db.session.add(self.test_user)
            db.session.commit()
            self.user_registry = self.test_user.query.get(self.test_user.id)
            self.request_user = Request(
                meal_type="Dinner",
                location_request="Denver",
                latitud="4.523232",
                meal_time=datetime.now(),
                filled=10,
                filled_limit = True,
                user = self.user_registry
            )
            db.session.add(self.request_user)
            db.session.commit()
            insert_registry = len(self.request_user.query.all())
            self.assertEqual(insert_registry, 1)

    def test_create_proposal_data_base(self):
        with self.app.app_context():
            self.test_user = User(
                name="Julian", 
                email="Juliansalas080@gmail.com",
                password_hash="1qwfsdafas",
                age=27
            )
            db.session.add(self.test_user)
            db.session.commit()
            self.user_registry = self.test_user.query.get(self.test_user.id)
            self.request_user = Request(
                meal_type="Dinner",
                location_request="Denver",
                latitud="4.523232",
                meal_time=datetime.now(),
                filled=10,
                filled_limit = True,
                user = self.user_registry
            )
            db.session.add(self.request_user)
            db.session.commit()
            self.proposal = Proposal(
                user_proposed_to=self.user_registry.id,
                request_id=self.request_user.id,
                user_proposed_from= self.request_user.user_id
            )
            db.session.add(self.proposal)
            db.session.commit()
            insert_registry = len(self.proposal.query.all())
            self.assertEqual(insert_registry, 1)
    
    def test_create_user(self):
        with self.app.app_context():
            query = {
	            "name":"Julian", 
	            "email":"Juliansalas080@gmail.com",
	            "password_hash":"1qwfsdafas",
	            "age":27
            }
            result = self.app_client.post(
                "api/v1/create/user", data=json.dumps(query),
                content_type='application/json'
            )
            data = json.loads(result.data.decode('utf-8'))
            self.assertEqual(result.status_code, 200)
            self.assertEqual(data, {
                "User": "Julian",
                "id": 1,
                "message": "Created User"
            })
        
            
        
# class TestApiRest(unittest.TestCase):
    
#     def setup(self):
#         #Here call environment testing setting.
#         self.app_v = create_app(os.getenv('FLASK_CONFIG_TESTING', default=None))
        
#     def test_create_user(self):
#         with self.app_v.app_context():
#             url = "http://localhost:9000"+API_INDEX+ "/create/user"
#             query = {
# 	            "name":"Julian", 
# 	            "email":"Juliansalas080@gmail.com",
# 	            "password_hash":"1qwfsdafas",
# 	            "age":27
	
#             }
#             response = requests.post(url, json=query)
#             self.assertEqual(response.status_code, 500)
#             self.assertEqual(reponse.json(), {
#                 "User": "Julian",
#                 "id": 2,
#                 "message": "Created User"
#             })
        

        
        
    



if __name__ == '__main__':
    unittest.main()

    


