from datetime import datetime
from flask import Flask, jsonify, request, url_for, abort, make_response
from flask_api import status
import logging
import os
import json

from app.util import initialize_logging
from app.models import Promotion

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
    #TODO
    filters = dict(request.args)
    promos = Promotion.query(filters)
    payload = [promo.serialize() for promo in promos]
    flask_app.logger.info("GET all promotions success")
    return jsonify(payload), 200

@flask_app.route('/promotions/<int:promo_id>', methods=['GET'])
def get_promotion(promo_id):
    '''Get a Promotion with id="promo_id" '''
    promos = Promotion.find_by_id(promo_id)
    if not promos: 
        info = 'Promotion with id: {} was not found'.format(promo_id)
        flask_app.logger.info(info)
        return jsonify(error=info), 404
    flask_app.logger.info("GET promotion with id: {} success".format(promo_id))
    return jsonify(promos[0].serialize()), 200

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
        message = promotion.serialize()
        response = make_response(jsonify(message), 201)
        response.headers['Location'] = url_for('get_promotion', promo_id=promotion.id, _external=True)
        return response
    except Exception as e:
        return jsonify(error=str(e)),400

@flask_app.route('/promotions/<int:promo_id>', methods=['PUT'])
def update_promotion(promo_id):
    '''Update an existing Promotion'''
    check_content_type('application/json')
    promos = Promotion.find_by_id(promo_id)
    if not promos: 
        info = 'Promotion with id: {} was not found'.format(promo_id)
        flask_app.logger.info(info)
        return jsonify(error=info), 404
    promo = promos[0]
    data = request.get_json()
    promo.deserialize(data)
    flask_app.logger.warning('Update Success')
    return jsonify(promo.serialize()), 200

@flask_app.route('/promotions/<int:promo_id>', methods=['DELETE'])
def delete_promotion(promo_id):
    '''Delete an existing Promotion'''
    promos = Promotion.find_by_id(promo_id)
    if promos:
        promos[0].delete()
    return '', 204

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
