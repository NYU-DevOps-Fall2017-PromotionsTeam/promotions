from flask import Flask, jsonify, request, url_for
import os

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

if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
