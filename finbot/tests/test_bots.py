from django.test import TestCase
from finbot.utils import finbot


class TestFinBot(TestCase):

    def test_stock_command(self):
        finbot_respose = finbot('/stock=FB')
        fields = {'timestamp',
                  'message',
                  'username'}
        self.assertEqual(set(finbot_respose), fields)
        self.assertEqual(finbot_respose['username'], 'finbot')
        self.assertIn('Facebook', finbot_respose['message'])

    def test_day_range_command(self):
        finbot_respose = finbot('/day_range=FB')
        fields = {'timestamp',
                  'message',
                  'username'}
        self.assertEqual(set(finbot_respose), fields)
        self.assertEqual(finbot_respose['username'], 'finbot')
        self.assertIn('Facebook', finbot_respose['message'])    
        self.assertIn('Low', finbot_respose['message'])    
        self.assertIn('High', finbot_respose['message'])    
