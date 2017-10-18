from datetime import datetime, date
from datetime import timedelta
import json
import os
import unittest

from promotion import Promotion
from server import flask_app

from server import list_promotions, \
    get_promotion, create_promotion, update_promotion, delete_promotion, check_content_type

class TestServer(unittest.TestCase):

    def setUp(self):
        self.app = flask_app.test_client()

    def tearDown(self):
        pass

    def test_list_promotions(self):
        '''Test list all promotions'''
        resp = self.app.get('/promotions')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(data, [])
        for i in range(5):
            self.app.post('/promotions', data=json.dumps({}), content_type='application/json')
        resp = self.app.get('/promotions')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(len(data), 5)
        # Clean up 
        Promotion.data = []

    def test_get_promotion(self):
        '''Test Getting the Promo with ID = 1 '''
        promo = Promotion()
        promo.id = 1
        promo.save()
        resp = self.app.get('/promotions/1')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(data['name'], 'default')
        promo.delete()

    def test_bad_get_by_id(self):
        '''Bad get by Id'''
        promo = Promotion()
        promo.id = 12
        promo.save()
        resp = self.app.get('/promotions/13')
        self.assertEqual(resp.status_code, 404)
        promo.delete()

    def test_create_promotion(self):
        '''Test Creating simple promotion & one with attributes'''
        response = self.app.post('/promotions', data=json.dumps({}), content_type='application/json')
        # Get promotion back
        promo = Promotion.all()[0]
        self.assertIsNotNone(promo)
        self.assertEqual(promo.name, 'default')
        self.assertEqual(promo.promo_type, '$')
        self.assertIsInstance(promo.value, float)
        self.assertEqual(promo.value, 0.0)
        self.assertEqual(promo.detail, 'n/a')
        self.assertEqual(promo.start_date, datetime.max)
        self.assertEqual(promo.end_date, datetime.max)
        promo.delete()
    
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
        # Get promotion back from Model
        promo = Promotion.all()[0]
        self.assertIsNotNone(promo)
        self.assertEqual(promo.name, 'test')
        self.assertEqual(promo.promo_type, '%')
        self.assertIsInstance(promo.value, float)
        self.assertEqual(promo.value, 10.0)
        self.assertEqual(promo.detail, 'test')
        self.assertEqual(promo.start_date, datetime(2017, 1, 1, 11, 11, 11))
        self.assertEqual(promo.end_date, datetime(2018, 2, 2, 11, 11, 11))
        promo.delete()

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

    def test_update_promotion(self):
        '''Do a put to update some data'''
        params = {
            'name': "OLDNAME",
            'value': 10,
            'detail': 'test'
        }
        response = self.app.post('/promotions', data=json.dumps(params), content_type='application/json')
        promo = Promotion.all()[0]
        self.assertEqual(promo.name, 'OLDNAME')
        _id = promo.id
        data = {'name': 'NEWNAME'}
        response = self.app.put('/promotions/'+str(_id), data=json.dumps(data), content_type='application/json')
        promo = Promotion.all()[0]
        self.assertEqual(promo.name, 'NEWNAME')
        promo.delete()

    def test_bad_update(self):
        '''Test Bad update, ID not found'''
        promo = Promotion()
        promo.name = 'OLDNAME'
        promo.id = 99
        promo.save()
        data = {'name': 'NEWNAME'}
        resp = self.app.put('/promotionsi/'+str(100), data=json.dumps(data), content_type='application/json')
        self.assertEqual(promo.name, 'OLDNAME')
        self.assertEqual(resp.status_code, 404)
        promo.delete()

    def test_delete_promotion(self):
        '''Test Delete'''
        resp = self.app.delete('/promotions/%d' % 100)
        self.assertEqual(Promotion.all(), [])
        self.assertEqual(resp.status_code, 200)
        self.app.post('/promotions', data=json.dumps({}), content_type='application/json')
        self.assertEqual(len(Promotion.all()), 1)
        promo = Promotion.all()[0]
        _id = promo.id
        resp = self.app.delete('/promotions/%d' % _id)
        self.assertEqual(Promotion.all(), [])
        self.assertEqual(resp.status_code, 200)
        

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
        promo.delete()

    def test_check_content_type(self):
        resp = self.app.post('/promotions', data=json.dumps({}), content_type='application/xml')
        self.assertEqual(resp.status_code, 415)
        resp = self.app.post('/promotions', data=json.dumps({}), content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        Promotion.data = []


if __name__ == '__main__':
    unittest.main()
