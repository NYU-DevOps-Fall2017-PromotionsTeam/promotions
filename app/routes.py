import datetime
from flask import Flask, jsonify, request, url_for
from .main import flask_app
import os

from promotions import Promotion

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

@flask_app.route('/promotions', methods=['GET'])
def index():
    '''List all available Promotions'''
    promos = Promotion.all()
    # TODO(joe): Add filters here??
    results = [promo.serialize() for promo in promos]
    return jsonify(payload), 200

@flask_app.route('/promotions/<int:promo_id>', methods=['GET'])
def get_promotion(promo_id):
    '''Get a Promotion with id="promo_id" '''
    pass

@flask_app.route('/promotions', methods=['POST'])
def create_promotion():
    '''Create a New Promotion'''
    start_date = datetime.datetime.now().date()
    promotion = Promotion()
    name = request.args.get('name')
    value = requests.args.get('value')
    promo_type = requests.args.get('type')
    data = {]
    data['name'] = name or 'NONE'
    data['value'] = value or 'NONE'
    data['promo_type'] = promo_type or 'NONE'
    flask_app.logger.info(data)
    return jsonify(data), 200

@flask_app.route('/promotions/<int:promo_id>', methods=['PUT'])
def update_promotion(promo_id):
    '''Update an existing Promotion'''
    pass

@flask_app.route('/promotions/<int:promo_id>', methods=['DELETE'])
def delete_promotion(promo_id):
    '''Delete an existing Promotion'''
    pass
