from flask import Flask, jsonify, request, url_for
from .main import flask_app
import os

"""
Promotion  Service

Available Resources:
------
GET /promotions - Returns a list all of the Active Promotions
GET /promotions/{id} - Returns the Pet with a given promot-id number
                       Almost Like a "PromoCode"
POST /promotion - creates a new Promotion in the database
PUT /promotion/{id} - updates a Promotion record in the database
DELETE /pets/{id} - deletes a Promotion record in the database
"""

# Flask Main App Route
# See routes.py for Business Logic / Path code

@flask_app.route('/promotions')
def index():
    '''Returns a message about the service'''
    payload = {}
    payload['info'] = 'Promotion Service Main Page!'
    payload['data'] = {"Urls": "Put Something Here"}
    payload['version'] = '1.0'
    return jsonify(payload), 200

@flask_app.route('/promotions/<int:promo_id>', methods=['GET'])
def get_promotion(promo_id):
    '''Get a Promotion with id="promo_id" '''
    pass

@flask_app.route('/promotions', methods=['POST'])
def get_promotion(promo_id):
    '''Create a New Promotion'''
    pass

@flask_app.route('/promotions/<int:promo_id>', methods=['PUT'])
def get_promotion(promo_id):
    '''Update an existing Promotion'''
    pass

@flask_app.route('/promotions/<int:promo_id>', methods=['DELETE'])
def get_promotion(promo_id):
    '''Delete an existing Promotion'''
    pass