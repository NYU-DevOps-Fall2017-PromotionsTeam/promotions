import logging
import os

from flask import Flask, jsonify, request, redirect, abort, make_response
from flask_restplus import Api, Resource, fields

from app.util import initialize_logging
from app.models import Promotion

# Get bindings from the env
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5001')  # NOTICE PORT 5001 !!!!
HOSTNAME = os.getenv('HOSTNAME', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

# SETUP INITIAL APP
flask_app = Flask(__name__)

# Redirect Root URL to new Home Url /promotions/home


@flask_app.route('/')
def index():
    return flask_app.send_static_file('index.html')

######################################################################
# Configure Swagger before initilaizing it
######################################################################
api = Api(flask_app,
          version='1.0.0',
          title='Promotion Service REST API',
          description='Serving data on what promotions are available',
          doc='/promotions/api'
          )

# This namespace is the start of the path i.e., /promotions
ns = api.namespace('promotions', description='Promotion operations')

# Define the model so that the docs reflect what can be sent
promotion_model = api.model('Promotion', {
    'id': fields.Integer(readOnly=True,
                         description='The unique id assigned internally by service'),
    'name': fields.String(required=True,
                          description='The name of the Promotion, "default" if not defined by user'),
    'promo_type': fields.String(required=True,
                                description='The type of the Promotion, either "%" or "$" '),
    'value': fields.Float(required=True,
                          description='The Value of the current deal, "10.50" or "1"'),
    'start_date': fields.String(required=True,
                                description='Date when the promotion is valid from, YYYY-MM-DD HH:MM:SS'),
    'end_date': fields.String(required=True,
                              description='Date when the promotion is valid to, YYYY-MM-DD HH:MM:SS'),
    'detail': fields.String(required=True,
                            description='Details describing the Current Promotion')
})


@ns.route('/<int:promo_id>', strict_slashes=False)
class PromotionResource(Resource):

    """
    PromotionResource class
    Allows the manipulation of a single Promotion
    GET /promotion{id} - Returns a promotion with the id
    PUT /promotion{id} - Update a promotion with the id
    DELETE /promotion{id} -  Deletes a promotion with the id
    """

    #-----------------------------------------
    # GET PROMOTION BY ID
    #-----------------------------------------
    @ns.doc('get_a_promotion')
    @ns.response(404, 'Promotion not found')
    def get(self, promo_id):
        '''Returns all Promotions'''
        promo = Promotion.find_by_id(promo_id)
        print("PROMO:", promo)
        if not promo:
            info = 'Promotion with id: {} was not found'.format(promo_id)
            flask_app.logger.info(info)
            return make_response(jsonify(error=info), 404)
        flask_app.logger.info(
            "GET promotion with id: {} success".format(promo_id))
        return make_response(jsonify(promo.serialize()), 200)

    #-----------------------------------------
    # UPDATE PROMOTION WITH ID
    #-----------------------------------------
    @ns.doc('update_promotion')
    @ns.response(404, 'Promotion not found')
    @ns.response(400, 'The posted Promotion data was not valid')
    @ns.response(415, 'Invalid Content Type')
    def put(self, promo_id):
        '''Update a single promotion'''
        check_content_type('application/json')
        promo = Promotion.find_by_id(promo_id)
        if not promo:
            info = 'Promotion with id: {} was not found'.format(promo_id)
            flask_app.logger.info(info)
            return make_response(jsonify(error=info), 404)
        promo.deserialize(api.payload)
        promo.save()
        flask_app.logger.info('Update Success')
        return make_response(jsonify(promo.serialize()), 200)

    #-----------------------------------------
    # DELETE PROMOTION
    #-----------------------------------------
    @ns.doc('delete_promotion')
    @ns.response(204, 'Promotion deleted')
    def delete(self, promo_id):
        '''Delete a specific Promotion'''
        flask_app.logger.info('Request to Delete a promotion with id [%s]', id)
        promo = Promotion.find_by_id(promo_id)
        if promo:
            promo.delete()
        return make_response('', 204)


@ns.route('/', strict_slashes=False)
class PromotionCollection(Resource):
    """ Handles all interactions with collections of Promotions """

    @ns.doc('get_all_promotions')
    @ns.param('promo_type', 'List Promotion with this type')
    @ns.param('available_on', 'List Promotion available on this date')
    @ns.marshal_list_with(promotion_model, code=200)
    def get(self):
        """ Returns all of the Promotions """
        conditions = request.values.to_dict()
        payload = Promotion.all()

        if conditions:
            payload = Promotion.find_by_conditions(conditions)

        payload = [promo.serialize() for promo in payload]

        flask_app.logger.info("GET promotions success")

        return payload, 200

    @ns.doc('create_promotion')
    @ns.expect(promotion_model)
    @ns.response(400, 'The posted data was not valid')
    @ns.response(415, 'Invalid Content Type')
    @ns.response(201, 'Promotion created successfully')
    @ns.marshal_with(promotion_model, code=201)
    def post(self):
        """
        Creates a Promotion
        This endpoint will create a Promotion based the data in the body that is posted
        """
        check_content_type('application/json')
        try:
            promotion = Promotion()
            promotion.deserialize(api.payload)
            promotion.save()
            flask_app.logger.info('CREATE promotion Success')
            location_url = api.url_for(
                PromotionResource, promo_id=promotion.id, _external=True)
            return promotion.serialize(), 201, {'Location': location_url}
        except Exception as e:
            print("EXCEPTION:", str(e))
            return jsonify(error=str(e)), 400


@ns.route('/<string:action>', strict_slashes=False)
class ActionResource(Resource):

    def put(self, action):
        '''Perform Some action on the resource'''
        if action == 'delete-all':
            data_reset()
            return make_response('', 204)

#------------------------------------


@flask_app.before_first_request
def init_db(redis=None):
    ''' Initialize the model '''
    Promotion.init_db(redis)


def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] != content_type:
        flask_app.logger.error('Invalid Content-Type: %s' %
                               request.headers['Content-Type'])
        abort(415, 'Content-Type must be {}'.format(content_type))


def data_reset():
    Promotion.remove_all()


def data_load(promo_id, data):
    promo = Promotion(promo_id)
    promo.deserialize(data)
    promo.save()

def run():
    initialize_logging(logging.INFO, flask_app)
    flask_app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
