import os
import json
import unittest
from redis import Redis
from werkzeug.exceptions import NotFound
from app.models import Promotion, DataValidationError, DatabaseConnectionError
from app import server  # to get Redis
from datetime import datetime

VCAP_SERVICES = {
    'rediscloud': [
        {'credentials': {
            'password': '',
            'hostname': '127.0.0.1',
            'port': '6379'
            }
        }
    ]
}

class TestPromotion(unittest.TestCase):

    def setUp(self):
        Promotion.init_db()
        Promotion.remove_all()

    def test_serialize(self):
        promo = Promotion()
        data = {'id': promo.id, 'name': 'default', 'promo_type': '$', 'value': 0.0,
                'start_date': '9999-12-31 23:59:59', 'end_date': '9999-12-31 23:59:59', 'detail': 'n/a'}
        self.assertEqual(promo.serialize(), data)

    def test_save(self):
        promo = Promotion()
        self.assertEqual(len(Promotion.all()), 0)
        promo.save()        
        promos = Promotion.all()
        self.assertEqual(len(promos), 1)
        data = {'id': promo.id, 'name': 'default', 'promo_type': '$', 'value': 0.0,
                'start_date': '9999-12-31 23:59:59', 'end_date': '9999-12-31 23:59:59', 'detail': 'n/a'}
        self.assertEqual(promos[0].serialize(), data)

    def test_delete(self):
        promo = Promotion()
        promo.save()
        self.assertEqual(len(Promotion.all()), 1)
        promo.delete()
        self.assertEqual(len(Promotion.all()), 0)

    def test_deserialize(self):
        promo = Promotion()
        data = {'name': 'test', 'promo_type': '%', 'value': 5.0, 'start_date': '2017-10-17 23:59:59',
                'end_date': '9999-12-31 23:59:59', 'detail': 'testtest'}
        promo.deserialize(data)
        self.assertEqual(promo.serialize(), {'id': promo.id, 'name': 'test', 'promo_type': '%', 'value': 5.0,
                                             'start_date': '2017-10-17 23:59:59', 'end_date': '9999-12-31 23:59:59', 'detail': 'testtest'})

    def test_query(self):
        '''
        with self.assertRaises(DataValidationError):
            Promotion.query([])
        with self.assertRaises(DataValidationError):
            Promotion.query({'promo_type': 'fail'})
        with self.assertRaises(DataValidationError):
            Promotion.query({'valid_on': 'fail'})
        with self.assertRaises(DataValidationError):
            Promotion.query({'discount_greater_or_equal': 'fail'})
        promo = Promotion()
        data = {'name': 'test', 'promo_type': '%', 'value': 5.0, 'start_date': '2017-10-17 23:59:59',
                'end_date': '9999-12-31 23:59:59', 'detail': 'testtest'}
        promo.deserialize(data)
        promo.save()
        self.assertIn(promo, Promotion.query({'name': 'es'}))
        self.assertIn(promo, Promotion.query({'promo_type': '%'}))
        self.assertIn(promo, Promotion.query({'discount_greater_or_equal': 4}))
        self.assertIn(promo, Promotion.query(
            {'valid_on': '2017-10-18 12:59:59'}))
        self.assertIn(promo, Promotion.query({'detail': 'test'}))

        self.assertNotIn(promo, Promotion.query({'name': 'fail'}))
        self.assertNotIn(promo, Promotion.query({'promo_type': '$'}))
        self.assertNotIn(promo, Promotion.query(
            {'discount_greater_or_equal': 6}))
        self.assertNotIn(promo, Promotion.query(
            {'valid_on': '2017-10-17 12:59:59'}))
        self.assertNotIn(promo, Promotion.query({'detail': 'fail'}))
        '''
        pass

    def test_find_by_id(self):
        promo = Promotion()
        promo.save()
        promo_id = promo.id
        fake_id = promo_id - 1
        test = Promotion.find_by_id(promo_id)
        self.assertIsNotNone(test)
        self.assertEqual(test.id, promo_id)
        failtest = Promotion.find_by_id(fake_id)
        self.assertIsNone(failtest)

    def test_passing_connection(self):
        """ Pass in the Redis connection """
        Promotion.init_db(Redis(host='127.0.0.1', port=6379))
        self.assertIsNotNone(Promotion.redis)

    def test_passing_bad_connection(self):
        """ Pass in a bad Redis connection """
        self.assertRaises(DatabaseConnectionError, Promotion.init_db, Redis(host='127.0.0.1', port=6300))
        self.assertIsNone(Promotion.redis)

if __name__ == '__main__':
    unittest.main()
