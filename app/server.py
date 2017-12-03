import logging
import os

from flask import Flask, jsonify, request, url_for, abort, make_response
from flask_api import status
from flask_restplus import Api, Resource, fields

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
PUT /promotions/delete-all - delete all promotions in the database
"""

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return True
    flask_app.logger.error('Invalid Content-Type: %s' % request.headers['Content-Type'])
    abort(415, 'Content-Type must be {}'.format(content_type))

@flask_app.route('/', methods=['GET'])
def index():
    '''The Root URL for Promotion Service'''
    return flask_app.send_static_file('index.html')
    
@flask_app.route('/promotions', methods=['GET'])
def list_promotions():
    '''List all available Promotions'''
    #TODO
    #filters = dict(request.args)
    #promos = Promotion.query(filters)
    payload = Promotion.all()
    payload = [promo.serialize() for promo in payload]
    flask_app.logger.info("GET all promotions success")
    return jsonify(payload), 200

@flask_app.route('/promotions/<int:promo_id>', methods=['GET'])
def get_promotion(promo_id):
    '''Get a Promotion with id="promo_id" '''
    promo = Promotion.find_by_id(promo_id)
    if not promo: 
        info = 'Promotion with id: {} was not found'.format(promo_id)
        flask_app.logger.info(info)
        return jsonify(error=info), 404
    flask_app.logger.info("GET promotion with id: {} success".format(promo_id))
    return jsonify(promo.serialize()), 200

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
        return jsonify(error=str(e)), 400

@flask_app.route('/promotions/<int:promo_id>', methods=['PUT'])
def update_promotion(promo_id):
    '''Update an existing Promotion'''
    check_content_type('application/json')
    promo = Promotion.find_by_id(promo_id)
    if not promo: 
        info = 'Promotion with id: {} was not found'.format(promo_id)
        flask_app.logger.info(info)
        return jsonify(error=info), 404
    data = request.get_json()
    promo.deserialize(data)
    promo.save()
    flask_app.logger.warning('Update Success')
    return jsonify(promo.serialize()), 200

@flask_app.route('/promotions/<int:promo_id>', methods=['DELETE'])
def delete_promotion(promo_id):
    '''Delete an existing Promotion'''
    promo = Promotion.find_by_id(promo_id)
    if promo:
        promo.delete()
    return '', 204

@flask_app.route('/promotions/delete-all', methods=['PUT'])
def delete_all_promotions():
    '''Clean out the Current Model and delete all objects contained'''
    Promotion.remove_all()
    return make_response(jsonify(''), status.HTTP_204_NO_CONTENT)

@flask_app.before_first_request
def init_db(redis=None):
    """ Initialize the model """
    Promotion.init_db(redis)

def data_reset():
    Promotion.remove_all()

def data_load(promo_id,data):
    promo = Promotion(promo_id)
    promo.deserialize(data)
    promo.save()

if __name__ == "__main__":
    initialize_logging(logging.INFO, flask_app)
    flask_app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
