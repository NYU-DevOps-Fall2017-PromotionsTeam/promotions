from datetime import datetime
from flask import Flask, jsonify, request, url_for, abort, make_response
from flask_api import status
import logging
import os
import json

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

GET /promotions - Returns a list all of the Active Promotions
GET /promotions/{id} - Returns the Pet with a given promot-id number
                       Almost Like a "PromoCode"
POST /promotions - creates a new Promotion in the database
PUT /promotions/{id} - updates a Promotion record in the database
DELETE /promotions/{id} - deletes a Promotion record in the database
PUT /promotions/write-to-file - writes the current State of the promo model to a file
"""

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return True
    flask_app.logger.error('Invalid Content-Type: %s' % request.headers['Content-Type'])
    abort(415, 'Content-Type must be {}'.format(content_type))

@flask_app.route('/promotions', methods=['GET'])
def list_promotions():
    '''List all available Promotions'''
    filters = dict(request.args)
    promos = Promotion.query(filters)
    payload = [promo.serialize() for promo in promos]
    flask_app.logger.info("GET all promotions success")
    return jsonify(payload), status.HTTP_200_OK

@flask_app.route('/promotions/<int:promo_id>', methods=['GET'])
def get_promotion(promo_id):
    '''Get a Promotion with id="promo_id" '''
    promos = Promotion.find_by_id(promo_id)
    if not promos: 
        info = 'Promotion with id=%s not found' % promo_id
        return jsonify(info), status.HTTP_404_NOT_FOUND
    flask_app.logger.info("GET promotion with id: {} success".format(promo_id))
    return jsonify(promos[0].serialize()), status.HTTP_200_OK

@flask_app.route('/promotions', methods=['POST'])
def create_promotion():
    '''Create a New Promotion'''
    check_content_type('application/json')
    data = request.get_json()
    try:
        promotion = Promotion()
        promotion.deserialize(data)
        promotion.save()
        flask_app.logger.info('CREATE promotion Success')
        return jsonify(promotion.serialize()), status.HTTP_201_CREATED
    except Exception as e:
        flask_app.logger.info('CREATE promotion failed with error: '+str(e))
        return jsonify(error=str(e)), status.HTTP_400_BAD_REQUEST

@flask_app.route('/promotions/<int:promo_id>', methods=['PUT'])
def update_promotion(promo_id):
    '''Update an existing Promotion'''
    check_content_type('application/json')
    promos = Promotion.find_by_id(promo_id)
    if not promos: 
        info = 'Promotion with id=%s not found' % promo_id
        flask_app.logger.info(info)
        return jsonify(status=404, error='Not Found', message=info), 404
    promo = promos[0]
    data = request.get_json()
    promo.deserialize(data)
    flask_app.logger.warning('Update Success')
    return jsonify(promo.serialize()), status.HTTP_200_OK

@flask_app.route('/promotions/<int:promo_id>', methods=['DELETE'])
def delete_promotion(promo_id):
    '''Delete an existing Promotion'''
    flask_app.logger.info('Request to delete Promo with id: {}'.format(promo_id))
    promos = Promotion.find_by_id(promo_id)
    if promos:
        promos[0].delete()
    return make_response('', status.HTTP_204_NO_CONTENT)

@flask_app.route('/promotions/write-to-file', methods=['PUT'])
def perform_action():
    '''Perform some action on the Promotion Model
       action being implemented: write all promotions in JSON format to a file
    '''
    with open('data.txt', 'w') as outfile:
        data = [promo.serialize() for promo in Promotion.all()]
        json.dump(data, outfile)
    return make_response('', 204)

if __name__ == "__main__":
    initialize_logging(logging.INFO, flask_app)
    flask_app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
