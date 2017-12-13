import os
from behave import *
from app import server
from selenium import webdriver
import urllib.request

BASE_URL = os.getenv('BASE_URL', 'http://localhost:5001')

def before_all(context):
    context.app = server.flask_app.test_client()
    server.init_db()

    context.driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
    context.driver.implicitly_wait(10) # seconds
    context.driver.set_window_size(1120, 550)
    context.base_url = BASE_URL
