from flask import Flask, jsonify, request, url_for

flask_app = Flask(__name__)

# Get bindings from the env
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5001') # NOTICE PORT 5001 !!!! 
HOSTNAME = os.getenv('HOSTNAME', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

# Flask Routes

@app.route('/')
def index():
    '''Returns a message about the service'''
    return jsonify(name='You\'ve hit the Promo Service',
                   version='1.0',
                   url=url_for('hits', _external=True)
                  ), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
