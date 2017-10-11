import unittest
from promotion import Promotion

class TestCaseZero(unittest.TestCase):
  def setUp(self):
    self.promotion = Promotion()
    
  def tearDown(self):
    self.promotion = None
    
  '''List tests for each system functions'''
  def test_get_promotion(self, promo_id):
    resp = self.flask_app.get_promotion('/promotions/1')
    self.assertEqual(resp.status_code, 200)
    data = json.loads(resp.data)
    self.assertEqual(data['name'], 'promo_1')
    
if __name__ == '__main__': 
  unittest.main()
