from os import getenv
import requests
from behave import *
import json
from app import server

BASE_URL = getenv('BASE_URL', 'http://localhost:5001/')

@given(u'the following promotions')
def step_impl(context):

    # TODO(joe): Add code here to clear the Model of any data
    # Will need to do this after persistence is added
    for row in context.table:
        server.data_load(
            row['id'],
            {
            "name": row['name'],
            "promo_type": row['promo_type'],
            "value": float(row['value']),
            "start_date": row['start_date'],
            "end_date": row['end_date'],
            "detail": row['detail']
             }
        )
