import os
import json
import unittest
from unittest.mock import patch
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
        '''test query by promo type'''
        promo1 = Promotion(1)
        promo2 = Promotion(2)
        promo1.deserialize({'promo_type': '%'})
        promo2.deserialize({'promo_type': '$'})
        promo1.save()
        promo2.save()
        test = Promotion.find_by_conditions({'promo_type': '$'})
        self.assertIsInstance(test, list)
        self.assertEqual(len(test), 1)
        self.assertEqual(test[0].id, 2)

        test2 = Promotion.find_by_conditions({'promo_type': '%'})
        self.assertIsInstance(test, list)
        self.assertEqual(len(test), 1)
        self.assertEqual(test2[0].id, 1)

    def test_query_2(self):
        '''test query by available on'''
        promo1 = Promotion(1)
        promo2 = Promotion(2)
        promo1.deserialize(
            {'start_date': '2017-01-01 00:00:00', 'end_date': '2019-01-01 00:00:00'})
        promo2.deserialize(
            {'start_date': '2018-01-01 00:00:00', 'end_date': '2020-01-01 00:00:00'})
        promo1.save()
        promo2.save()
        test = Promotion.find_by_conditions(
            {'available_on': '2016-01-01 00:00:00'})
        self.assertIsInstance(test, list)
        self.assertEqual(len(test), 0)

        test2 = Promotion.find_by_conditions(
            {'available_on': '2017-06-01 00:00:00'})
        self.assertIsInstance(test2, list)
        self.assertEqual(len(test2), 1)
        self.assertEqual(test2[0].id, 1)

        test3 = Promotion.find_by_conditions(
            {'available_on': '2018-06-01 00:00:00'})
        self.assertIsInstance(test3, list)
        self.assertEqual(len(test3), 2)

        test4 = Promotion.find_by_conditions(
            {'available_on': '2019-06-01 00:00:00'})
        self.assertIsInstance(test4, list)
        self.assertEqual(len(test4), 1)
        self.assertEqual(test4[0].id, 2)

    def test_query_3(self):
        '''test query by multiple conditions'''
        promo1 = Promotion(1)
        promo2 = Promotion(2)
        promo1.deserialize(
            {'promo_type': '%', 'start_date': '2017-01-01 00:00:00', 'end_date': '2019-01-01 00:00:00'})
        promo2.deserialize(
            {'promo_type': '$', 'start_date': '2018-01-01 00:00:00', 'end_date': '2020-01-01 00:00:00'})
        promo1.save()
        promo2.save()

        test = Promotion.find_by_conditions(
            {'promo_type': '$', 'available_on': '2017-06-01 00:00:00'})
        self.assertIsInstance(test, list)
        self.assertEqual(len(test), 0)

        test2 = Promotion.find_by_conditions(
            {'promo_type': '%', 'available_on': '2018-06-01 00:00:00'})
        self.assertIsInstance(test2, list)
        self.assertEqual(len(test2), 1)
        self.assertEqual(test2[0].id, 1)

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
        self.assertRaises(DatabaseConnectionError,
                          Promotion.init_db, Redis(host='127.0.0.1', port=6300))
        self.assertIsNone(Promotion.redis)

    @patch.dict(os.environ, {'VCAP_SERVICES': json.dumps(VCAP_SERVICES)})
    def test_vcap_services(self):
        """ Test if VCAP_SERVICES works """
        Promotion.init_db()
        self.assertIsNotNone(Promotion.redis)

    @patch('redis.Redis.ping')
    def test_redis_connection_error(self, ping_error_mock):
        """ Test a Bad Redis connection """
        ping_error_mock.side_effect = DatabaseConnectionError()
        self.assertRaises(DatabaseConnectionError, Promotion.init_db)
        self.assertIsNone(Promotion.redis)

if __name__ == '__main__':
    unittest.main()
