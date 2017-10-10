from datetime import datetime
from flask import Flask, jsonify, request, url_for
import logging
import os
from util import initialize_logging

from promotion import Promotion

flask_app = Flask(__name__)

# Get bindings from the env
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5001') # NOTICE PORT 5001 !!!! 
HOSTNAME = os.getenv('HOSTNAME', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

"""
Promotion  Service

Available Resources:
------
GET /promotions - Returns a list all of the Active Promotions
GET /promotions/{id} - Returns the Pet with a given promot-id number
                       Almost Like a "PromoCode"
POST /promotions - creates a new Promotion in the database
PUT /promotions/{id} - updates a Promotion record in the database
DELETE /promotions/{id} - deletes a Promotion record in the database
"""


@flask_app.route('/promotions', methods=['GET'])
def index():
    '''List all available Promotions'''
    promos = Promotion.all()
    # TODO(joe): Add filters here??
    payload = [promo.serialize() for promo in promos]
    return jsonify(payload), 200

@flask_app.route('/promotions/<int:promo_id>', methods=['GET'])
def get_promotion(promo_id):
    '''Get a Promotion with id="promo_id" '''
    promo = Promotion.find(promo_id)
    if not promo: 
        raise exception.NotFound('Promo with id: {} was not found'.format(promo_id))
    return jsonify(promo.serialize()), status.HTTP_200_OK

@flask_app.route('/promotions', methods=['POST'])
def create_promotion():
    '''Create a New Promotion'''
    # Fill dict with promotion params
    data = {}
    data['name'] = request.args.get('name')
    data['value'] = request.args.get('value')
    data['promo_type'] = request.args.get('type')
    data['start_date'] = datetime.now().date()
    data['detail'] = request.args.get('detail') or None
    promotion = Promotion(**data) # pass dict as params for **kwargs
    promotion.save()
    flask_app.logger.info(data)
    return jsonify(data), 201

@flask_app.route('/promotions/<int:promo_id>', methods=['PUT'])
def update_promotion(promo_id):
    '''Update an existing Promotion'''
    pass

@flask_app.route('/promotions/<int:promo_id>', methods=['DELETE'])
def delete_promotion(promo_id):
    '''Delete an existing Promotion'''
    pass

if __name__ == "__main__":
    initialize_logging(logging.INFO, flask_app)
    flask_app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
