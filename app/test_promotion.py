import unittest
from promotion import DataValidationError, Promotion
from datetime import datetime


class TestPromotion(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        Promotion.data = []

    def test_serialize(self):
        promo = Promotion()
        data = {'id': promo.id, 'name': 'default', 'promo_type': '$', 'value': 0.0,
                'start_date': '9999-12-31 23:59:59', 'end_date': '9999-12-31 23:59:59', 'detail': 'n/a'}
        self.assertEqual(promo.serialize(), data)

    def test_save(self):
        promo = Promotion()
        promo.save()
        self.assertIn(promo, Promotion.data)

    def test_delete(self):
        promo = Promotion()
        promo.save()
        promo.delete()
        promo2 = Promotion()
        promo2.delete()
        self.assertNotIn(promo, Promotion.data)
        self.assertNotIn(promo2, Promotion.data)
        self.assertEqual(Promotion.data, [])

    def test_deserialize(self):
        promo = Promotion()
        with self.assertRaises(DataValidationError):
            promo.deserialize([])
        with self.assertRaises(DataValidationError):
            promo.deserialize({'promo_type': 'fail'})
        with self.assertRaises(DataValidationError):
            promo.deserialize({'value': 'fail'})
        with self.assertRaises(DataValidationError):
            promo.deserialize({'start_date': 'fail'})
        with self.assertRaises(DataValidationError):
            promo.deserialize({'end_date': 'fail'})
        data = {'name': 'test', 'promo_type': '%', 'value': 5.0, 'start_date': '2017-10-17 23:59:59',
                'end_date': '9999-12-31 23:59:59', 'detail': 'testtest'}
        promo.deserialize(data)
        self.assertEqual(promo.serialize(), {'id': promo.id, 'name': 'test', 'promo_type': '%', 'value': 5.0,
                                             'start_date': '2017-10-17 23:59:59', 'end_date': '9999-12-31 23:59:59', 'detail': 'testtest'})

    def test_all(self):
        promo = Promotion()
        promo2 = Promotion()
        promo3 = Promotion()
        promo.save()
        promo2.save()
        promo3.save()
        self.assertEqual(len(Promotion.data), 3)
        self.assertIn(promo, Promotion.data)
        self.assertIn(promo2, Promotion.data)
        self.assertIn(promo3, Promotion.data)

    def test_query(self):
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

    def test_find_by_id(self):
        promo = Promotion()
        promo.save()
        promo_id = promo.id
        fake_id = promo_id - 1
        self.assertIn(promo, Promotion.find_by_id(promo_id))
        self.assertNotIn(promo, Promotion.find_by_id(fake_id))

if __name__ == '__main__':
    unittest.main()
