import unittest
from promotion import Promotion

class TestCaseZero(unittest.TestCase):
  def setUp(self):
    self.promotion = Promotion()
    
  def tearDown(self):
    self.promotion = None
    
  '''List tests for each system functions'''
    
if __name__ == '__main__': 
  unittest.main()
