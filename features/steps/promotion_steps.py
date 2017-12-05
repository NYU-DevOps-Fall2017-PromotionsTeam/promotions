from os import getenv
import requests
from behave import *
import json
from app import server

BASE_URL = getenv('BASE_URL', 'http://localhost:5001/')
#BASE_URL = getenv('BASE_URL', '/')

#########################################
# GIVEN STATEMENTS                      #
#########################################

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

#########################################
# WHEN STATEMENTS                       #
#########################################

@when(u'I visit "{page}"')
def step_impl(context, page):
    # print("Targer URL", BASE_URL +'{}'.format(page))
    context.resp = context.app.get(BASE_URL +'{}'.format(page))

@when(u'I visit the root url')
def step_impl(context):
    context.resp = context.app.get(BASE_URL)

@when(u'I retrieve "{url}" with id "{id}"')
def step_impl(context, url, id):
    target_url = '{}/{}'.format(url, id)
    context.resp = context.app.get(BASE_URL + target_url)
    context.data = json.loads(context.resp.data.decode('utf-8'))
    assert isinstance(context.data, dict)

@when(u'I update "{url}" with id "{id}"')
def step_impl(context, url, id):
    target_url = '{}/{}'.format(url, id)
    headers = {'content-type': 'application/json'}
    data = json.dumps(context.data)
    context.resp = context.app.put(BASE_URL + target_url, data=data, headers=headers)
    assert context.resp.status_code == 200

@when(u'I change "{key}" to "{value}"')
def step_impl(context, key, value):
    if key == 'value':
        value = float(value)
    context.data[key] = value

@when(u'I delete "{url}" with id "{id}"')
def step_impl(context, url, id):
    target_url = '{}/{}'.format(url, id)
    context.resp = context.app.delete(BASE_URL + target_url)
    assert context.resp.status_code == 204

@when(u'I create a promotion')
def step_impl(context):
    target_url = 'promotions'
    headers = {'content-type': 'application/json'}
    data=json.dumps({})
    context.resp = context.app.post(BASE_URL + target_url, data=data, headers=headers)

@when(u'I call POST with Incorrect content-type')
def step_impl(context):
    target_url = 'promotions'
    #headers = {'content-type': 'application/json'}
    headers = {'content-type': 'not_application/json'}
    data=json.dumps({})
    context.resp = context.app.post(BASE_URL + target_url, data=data, headers=headers)

@when(u'I send a PUT request to \'/promotions/delete-all\'')
def step_impl(context):
    target_url = 'promotions/delete-all'
    context.resp = context.app.put(BASE_URL + target_url)

#########################################
# THEN STATEMENTS                       #
#########################################

@then(u'I should get a response code "{code}"')
def step_impl(context, code):
    code = int(code)
    assert context.resp.status_code == code

@then(u'There should be "{count}" promotions')
def step_impl(context, count):
    count = int(count)
    data = json.loads(context.resp.data.decode('utf-8'))
    if isinstance(data, list):
        assert len(data) == count
    else:
        assert isinstance(data, dict)

@then(u'I should see "{promo_name}"')
def step_impl(context, promo_name):
    data = json.loads(context.resp.data.decode('utf-8'))
    if isinstance(data, list):
        names = [promo['name'] for promo in data]
        assert promo_name in names
    else:
        assert data['name'] == promo_name

@then(u'I should not see "{promo_name}"')
def step_impl(context, promo_name):
    data = json.loads(context.resp.data.decode('utf-8'))
    if isinstance(data, list):
        names = [promo['name'] for promo in data]
        assert promo_name not in names
    else:
        assert data['name'] != promo_name

@then(u'I will see "{promo_name}" with "{key}" as "{value}"')
def step_impl(context, promo_name, key, value):
    data = json.loads(context.resp.data.decode('utf-8'))
    if key == 'value':
        value = float(value)
    if isinstance(data, list):
        for promo in data:
            if promo['name'] == promo_name:
                assert promo[key] == value
                break
    else:
        assert data[key] == value

@then(u'I will not see a promotion with "{key}" as "{value}"')
def step_impl(context, key, value):
    data = json.loads(context.resp.data.decode('utf-8'))
    if key == 'value':
        value = float(value)
    if isinstance(data, list):
        for promo in data:
            assert promo[key] != value
    else:
        assert data[key] != value

@then(u'I reset the server db for further tests')
def step_impl(context):
    server.data_reset()