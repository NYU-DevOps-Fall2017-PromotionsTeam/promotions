from datetime import datetime, date
import json
import re
import os
import unittest

from app import server


class TestServer(unittest.TestCase):

    def setUp(self):
        '''Setup Test Model and Client'''
        self.app = server.flask_app.test_client()
        self.app.debug = False
        server.init_db()
        server.data_reset()
        server.data_load(1234,{'name':'test1'})
        server.data_load(5678,{'name':'test2'})

    def tearDown(self):
        server.data_reset()

    def test_index(self):
        '''Test list all promotions'''
        resp = self.app.get('/promotions/home')
        self.assertEqual(resp.status_code, 200)

    def test_list_promotions(self):
        '''Test list all promotions'''
        resp = self.app.get('/promotions')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        server.data_reset()
        resp = self.app.get('/promotions')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data, [])

    def test_get_promotion(self):
        '''Test Getting the Promo with ID = 1 '''
        resp = self.app.get('/promotions/1234')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertIsInstance(data, dict)
        self.assertEqual(data['name'], 'test1')
        self.assertEqual(data['id'], 1234)

    def test_bad_get_by_id(self):
        '''Bad get by Id'''
        info = 'Promotion with id: {} was not found'.format(13)
        resp = self.app.get('/promotions/13')
        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.data.decode('utf-8'))
        print("data", type(data))
        self.assertEqual(data['error'], info)

    def test_create_promotion(self):
        '''Test Creating simple promotion & one with attributes'''
        location_pattern = re.compile('http://localhost/promotions/\d*')
        response = self.app.post('/promotions', data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(location_pattern.match(response.headers['Location']))
        self.assertIsNotNone(response.data)

        data = json.loads(response.data.decode('utf-8'))
        promo_id = data['id']
        resp = self.app.get('/promotions/{}'.format(promo_id))
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get('/promotions')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)

    
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
        location_pattern = re.compile('http://localhost/promotions/\d*')
        self.assertTrue(location_pattern.match(response.headers['Location']))
        
        self.assertIsNotNone(resp_data)
        self.assertEqual(resp_data['name'], 'test')
        self.assertEqual(resp_data['promo_type'], '%')
        self.assertEqual(resp_data['value'], 10.0)
        self.assertEqual(resp_data['detail'], 'test')
        self.assertEqual(resp_data['start_date'], '2017-01-01 11:11:11')
        self.assertEqual(resp_data['end_date'], '2018-02-02 11:11:11')

        promo_id = resp_data['id']
        resp = self.app.get('/promotions/{}'.format(promo_id))
        self.assertEqual(resp.status_code, 200)

        resp = self.app.get('/promotions')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)

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
            'promo_type': 'A', # bad promo type
            'start_date': '2017-01-01 11:11:11',
            'end_date': '2018-02-02 11:11:11'
        }
        resp = self.app.post('/promotions', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400) 

        params = {
            'name': 'test',
            'value': "SOME STRING", # bad value type
            'detail': 'test',
            'promo_type': '%',
            'start_date': '2017-01-01 11:11:11',
            'end_date': '2018-02-02 11:11:11'
        }
        resp = self.app.post('/promotions', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, 400) 

    def test_update_promotion(self):
        '''Do a put to update some data'''
        data = {
            'name': "update_test",
            'value': 10,
            'end_date': '2018-02-02 11:11:11'
        }
        resp = self.app.put('/promotions/1234', data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(data['name'],'update_test')
        self.assertEqual(data['value'],10)
        self.assertEqual(data['end_date'], '2018-02-02 11:11:11')

        resp = self.app.get('/promotions')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        
    def test_bad_update(self):
        '''Test Bad update, ID not found'''
        data = {'name': 'NEWNAME'}
        resp = self.app.put('/promotions/'+str(100), data=json.dumps(data), content_type='application/json')
        self.assertEqual(resp.status_code, 404)

    def test_delete_promotion(self):
        '''Test Delete'''
        resp = self.app.delete('/promotions/{}'.format(8888))
        self.assertEqual(resp.status_code, 204)
        resp = self.app.get('/promotions')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        resp = self.app.delete('/promotions/{}'.format(1234))
        self.assertEqual(resp.status_code, 204)
        resp = self.app.get('/promotions')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

        resp = self.app.delete('/promotions/{}'.format(5678))
        self.assertEqual(resp.status_code, 204)
        resp = self.app.get('/promotions')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    def test_delete_all_promotions(self):
        '''Test action performed on Model (delete all)'''
        resp = self.app.put('/promotions/delete-all')
        self.assertEqual(resp.status_code, 204)
        resp = self.app.get('/promotions')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    def test_delete_all_promotions_fail(self):
        '''Test action performed on Model (delete all)'''
        resp = self.app.put('/promotions/delete-all')
        self.assertEqual(resp.status_code, 204)
        resp = self.app.get('/promotions')
        data = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)
        resp = self.app.put('/promotions/delete-all')
        self.assertEqual(resp.status_code, 204)

    def test_check_content_type(self):
        '''Basic Check to ensure util func is working'''
        resp = self.app.post('/promotions', data=json.dumps({}), content_type='application/xml')
        self.assertEqual(resp.status_code, 415)
        resp2 = self.app.post('/promotions', data=json.dumps({}), content_type='application/json')
        #print("RESP:", resp2)
        #print("RESP:", resp2.data)
        self.assertEqual(resp2.status_code, 201)


if __name__ == '__main__':
    unittest.main()
