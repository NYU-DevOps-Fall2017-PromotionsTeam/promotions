from datetime import datetime, date
import json
import re
import os
import unittest

from promotion import Promotion
from server import flask_app


class TestServer(unittest.TestCase):

    def setUp(self):
        '''Setup Test Model and Client'''
        self.app = flask_app.test_client()
        self.app.debug = False
        # TODO(joe): Change this when persistence is added
        Promotion.data = []

    def tearDown(self):
        '''TearDown Test Model'''
        # TODO(joe): Change this when persistence is added
        Promotion.data = [] # Final Clean up

    def test_list_promotions(self):
        '''Test list all promotions'''
        resp = self.app.get('/promotions')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(data, [])
        self.assertEqual(len(data), 0)
        Promotion().save()
        resp = self.app.get('/promotions')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_promotion(self):
        '''Test Getting the Promo with ID = 1 '''
        promo = Promotion()
        promo.id , promo.detail = 1, 'TEST'
        promo.save()
        resp = self.app.get('/promotions/1')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertIsInstance(data, dict)
        self.assertEqual(data['name'], 'default')
        self.assertEqual(data['detail'], 'TEST')
        self.assertEqual(data['value'], 0.0)
        self.assertEqual(data['id'], 1)

    def test_bad_get_by_id(self):
        '''Bad get by Id'''
        info = 'Promotion with id: {} was not found'.format(13)
        resp = self.app.get('/promotions/13')
        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(data['error'], info)

    def test_create_promotion(self):
        '''Test Creating simple promotion & one with attributes'''
        location_pattern = re.compile('http://localhost/promotions/\d*')
        response = self.app.post('/promotions', data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(location_pattern.match(response.headers['Location']))
        self.assertIsNotNone(response.data)
        resp_promo = json.loads(response.data.decode('utf-8'))
        self.assertEqual('default', resp_promo['name'])
        self.assertEqual('$', resp_promo['promo_type'])
        self.assertEqual(0.0, float(resp_promo['value']))
        self.assertEqual('n/a', resp_promo['detail'])
        self.assertEqual(resp_promo['start_date'], datetime.max.isoformat(sep=' ')[:19])
        self.assertEqual(resp_promo['end_date'], datetime.max.isoformat(sep=' ')[:19])
    
    def test_create_promotion2(self):
        '''Test Create With Parameters'''
        params = {
            'name': 'test',
            'value': 10.0,
            'detail': 'test',
            'promo_type': '%',
            'start_date': '2017-01-01 11:11:11',
            'end_date': '2018-02-02 11:11:11'
        }
        data = json.dumps(params)
        response = self.app.post('/promotions', data=data, content_type='application/json')
        resp_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(resp_data)
        self.assertEqual(resp_data['name'], 'test')
        self.assertEqual(resp_data['promo_type'], '%')
        self.assertIsInstance(float(resp_data['value']), float)
        self.assertEqual(float(resp_data['value']), 10.0)
        self.assertEqual(resp_data['detail'], 'test')
        self.assertEqual(resp_data['start_date'], datetime(2017, 1, 1, 11, 11, 11).isoformat(sep=' '))
        self.assertEqual(resp_data['end_date'], datetime(2018, 2, 2, 11, 11, 11).isoformat(sep=' '))

    def test_bad_create(self):
        '''bad creation'''
        params = {
            'name': 'test',
            'value': 10.0,
            'detail': 'test',
            'promo_type': '%',
            'start_date': '2017-01-0111:11:11', # notice bad time stamps
            'end_date': '2018-02-0211:11:11'
        }
        data = json.dumps(params)
        resp = self.app.post('/promotions', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400) 
        params = {
            'name': 'test',
            'value': 10.0,
            'detail': 'test',
            'promo_type': 'A',
            'start_date': '2017-01-01 11:11:11',
            'end_date': '2018-02-02 11:11:11'
        }
        resp = self.app.post('/promotions', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400) 
        params = {
            'name': 'test',
            'value': "SOME STRING",
            'detail': 'test',
            'promo_type': '%',
            'start_date': '2017-01-01 11:11:11',
            'end_date': '2018-02-02 11:11:11'
        }
        resp = self.app.post('/promotions', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400) 

    def test_update_promotion(self):
        '''Do a put to update some data'''
        params = {
            'name': "OLDNAME",
            'value': 10,
            'detail': 'test'
        }
        promo = Promotion()
        promo.deserialize(params)
        promo.save()
        _id = promo.id
        data = {'name': 'NEWNAME', 'value': 11, 'detail': 'TEST'}
        response = self.app.put('/promotions/'+str(_id), data=json.dumps(data), content_type='application/json')
        resp_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_data['name'], 'NEWNAME')
        self.assertEqual(float(resp_data['value']), 11)
        self.assertEqual(resp_data['detail'], 'TEST')

    def test_bad_update(self):
        '''Test Bad update, ID not found'''
        data = {'name': 'NEWNAME'}
        resp = self.app.put('/promotions/'+str(100), data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 404)

    def test_delete_promotion(self):
        '''Test Delete'''
        resp = self.app.delete('/promotions/%d' % 100)
        self.assertEqual(resp.status_code, 204)
        promo = Promotion()
        promo.save()
        _id = promo.id
        self.assertEqual(len(Promotion.data), 1)
        resp = self.app.delete('/promotions/%d' % _id)
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(len(Promotion.data),0)

    def test_write_to_file(self):
        '''Test Write to file'''
        promo = Promotion()
        promo.save()
        resp = self.app.put('/promotions/write-to-file')
        self.assertEqual(resp.status_code, 204)
        valid_text = json.dumps([promo.serialize()])
        with open('data.txt', 'r') as valid_file:
            test_text = valid_file.readline()
        self.assertEqual(valid_text, test_text)
        os.remove('./data.txt')  # Clean up

    def test_check_content_type(self):
        '''Basic Check to ensure util func is working'''
        resp = self.app.post('/promotions', data=json.dumps({}), content_type='application/xml')
        self.assertEqual(resp.status_code, 415)
        resp = self.app.post('/promotions', data=json.dumps({}), content_type='application/json')
        self.assertEqual(resp.status_code, 201)


if __name__ == '__main__':
    unittest.main()
