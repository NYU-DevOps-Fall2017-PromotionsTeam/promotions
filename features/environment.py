from behave import *
from app import server

def before_all(context):
    context.app = server.flask_app.test_client()
    server.init_db()