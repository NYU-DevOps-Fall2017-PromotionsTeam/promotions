from datetime import datetime, date
from datetime import timedelta
import unittest

from promotion import Promotion
from server import flask_app

from server import list_promotions, \
    get_promotion, create_promotion, update_promotion, delete_promotion

class TestServer(unittest.TestCase):

    def setUp(self):
        self.app = flask_app.test_client()

    def tearDown(self):
        pass

    def test_list_promotions(self):
        pass

    def test_get_promotion(self):
        '''Test Getting the Promo with ID = 1 '''
        resp = self.flask_app.get('/promotions/1')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'promo_1')

    def test_create_promotion(self):
        '''Test Creating simple promotion & one with attributes'''
        response = self.app.post('/promotions')
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
        params = '?name=test' \
                 '&value=10&detail=test&' \
                 'start_date=2017-01-01+11:11:11&end_date=2018-02-02+11:11:11&promo_type=%'
        response = self.app.post('/promotions'+params)
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

    def test_update_promotion(self):
        '''Do a put to update some data'''
        params = '?name=OLDNAME' \
                 '&value=10&detail=test&'
        response = self.app.post('/promotions'+params)
        promo = Promotion.all()[0]
        self.assertEqual(promo.name, 'OLDNAME')
        _id = promo.id
        response = self.app.put('/promotions/%d?name=NEWNAME' % _id)
        promo = Promotion.all()[0]
        self.assertEqual(promo.name, 'NEWNAME')
        promo.delete()

    def test_delete_promotion(self):
        resp = self.app.delete('/promotions/1')
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.status_code, 404)
if __name__ == '__main__':
    unittest.main()
