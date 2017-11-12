from behave import *
from app import server

def before_all(context):
    server.init_db()
    context.server = server