# -*- encoding: utf-8 -*-

# --*-- built-in packages --*--
from os import environ
# --*-- installed packages --*--
from marshmallow import ValidationError
from requests_oauthlib import OAuth2Session
import requests


# --*-- own packages --*--
from .models import User
from . import bcrypt



API_INDEX = "/api/v1/"


def must_not_be_blank(data):
    if not data:
        raise ValidationError("data not provided")




def get_geo_google_api(location):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        "address":location,
        "key":environ.get("SECRET_KEY_GOOGLE", None)
    }
    try:
        result = requests.get(url, params=params)
        latitud = result.json().\
            get("results")[0].get("geometry").get("location").get('lat', None)
        longitude = result.json().\
            get("results")[0].get("geometry").get("location").get('lng', None)
        return (latitud, longitude)
    except Exception as e:
        raise e
    

def find_restaurant_meet(meal_type, location):
    #environ.get("CLIENT_ID_FOURSQUARE",None)
    #environ.get("CLIENT_SECRET_FOURSQUARE",None)
    url = 'https://api.foursquare.com/v2/venues/search'
    lat, loc = location
    query = '{0},{1}'.format(lat,loc)
    params = {
        "client_id": 'U2UMZTPIRJOOGJ3XAH1TZJTAR1SCNTSXLO1Z2ELXYWRN5RQM',
        "client_secret":'Q1R4VUUQTKMKBVFK4YFMKCJTPRSOCZDV3ADRVSJBEWE2UXJI',
        "ll": query,
        "query": meal_type,
        "v": "20191016"
    }
    try:
        response = requests.get(url, params=params)
        data_to_restaurant =\
            process_data_find_restaurant_meet(response.json())
        return data_to_restaurant
    except Exception as e:
        raise e

def process_data_find_restaurant_meet(response):
    """Process data raw to get info about restaurant"""

    if not response.get('response').get('venues'):
        return None
    
    restaurant = response.get('response').get('venues')[0]
    restaurant_name = restaurant.get('name')
    venue_id = restaurant.get('id')
    restaurant_address = restaurant.get('location')\
        .get('formattedAddress')
    address = ""
    for name_rest in restaurant_address:
        address += name_rest + " "
    
    restaurant_address = address
    url_photo = 'https://api.foursquare.com/v2/venues/{0}/photos/'\
        .format(venue_id)
    params = {
        "client_id": 'U2UMZTPIRJOOGJ3XAH1TZJTAR1SCNTSXLO1Z2ELXYWRN5RQM',
        "client_secret":'Q1R4VUUQTKMKBVFK4YFMKCJTPRSOCZDV3ADRVSJBEWE2UXJI',
        "v": "20191016"
    }
    try:
        response = requests.get(url_photo, params=params)
        
    except Exception as e:
        raise e
    if response.json().get('response').get('photos').get('items'):
        print(response.json())
        pic = response.json().get('response').get('photos').get('items')[0]
        pic_prefix = pic.get('prefix')
        pic_suffix = pic.get('suffix')
        pic_url = pic_prefix + "300x300" + pic_suffix
    else:
        pic_url = 'http://oi43.tinypic.com/i6f4eq.jpg'
    
    data_restaurant = {
        'name': restaurant_name, 'address': restaurant_address, 
        'image': pic_url
    }
    return data_restaurant
        
        
            
        
        
    
    
    
    
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