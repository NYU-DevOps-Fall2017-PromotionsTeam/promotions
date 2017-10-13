from datetime import datetime, date
from datetime import timedelta
import unittest
from unittest import mock

from promotion import Promotion
from server import flask_app

from server import index, \
    get_promotion, create_promotion, update_promotion, delete_promotion

class TestServer(unittest.TestCase):

    def setUp(self):
        self.app = flask_app.test_client()

    def tearDown(self):
        pass

    def test_index(self):
        pass

    def test_get_promotion(self):
        pass

    def test_create_promotion(self):
        '''Test Creating simple promotion & one with attributes'''
        response = self.app.post('/promotions')
        # Get promotion back
        promo = Promotion.all()[0]
        self.assertIsNotNone(promo)
        self.assertEqual(promo.name, 'default')
        self.assertEqual(promo.promo_type, 'dollars')
        self.assertIsInstance(promo.value, float)
        self.assertEqual(promo.value, 0.0)
        self.assertEqual(promo.detail, 'n/a')
        self.assertEqual(promo.start_date, datetime.now().date())
        self.assertEqual(promo.end_date, datetime.max.date())
        promo.delete()
    
    def test_create_promotion2(self):
        '''Test Create With Parameters'''
        params = '?name=test' \
                 '&value=10&detail=test&' \
                 'start_date=01-01-17&end_date=02-02-18&promo_type=percent'
        response = self.app.post('/promotions'+params)
        # Get promotion back from Model
        promo = Promotion.all()[0]
        self.assertIsNotNone(promo)
        self.assertEqual(promo.name, 'test')
        self.assertEqual(promo.promo_type, 'percent')
        self.assertIsInstance(promo.value, float)
        self.assertEqual(promo.value, 10.0)
        self.assertEqual(promo.detail, 'test')
        self.assertEqual(promo.start_date, date(2017, 1, 1))
        self.assertEqual(promo.end_date, date(2018, 2, 2))
        promo.delete()

    def test_update_promotion(self):
        '''Do a put to update some data'''
        params = '?name=test' \
                 '&value=10&detail=test&'
        response = self.app.post('/promotions'+params)
        promo = Promotion.all()[0]
    #    self.assertIsNone(

    def test_delete_promotion(self):
        pass

if __name__ == '__main__':
    unittest.main()
