from datetime import datetime
from django.test import TestCase
from chat.factories import MessageFactory, UserFactory
from chat.models import Message


class MessageTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username='user')
        self.time = datetime.now()
        self.message = MessageFactory(user=self.user, 
                                      message='hello world', 
                                      timestamp=self.time)

    def tearDown(self):
        self.message.delete()

    def test_string_method(self):
        expected_str = 'user: hello world  [{}]'.format(
            self.time.strftime('%b %-d %-I:%M %p'))
        self.assertEqual(expected_str, self.message.__str__())

    def test_formatted_timestamp(self):
        time_formatted = self.time.strftime('%b %-d %-I:%M %p')
        self.assertEqual(time_formatted, self.message.formatted_timestamp)

    # Test if the as_dict method return attributes as a dict
    def test_as_dict(self):
        message_dict = {'username': 'user', 'message': 'hello world',
                        'timestamp': self.time.strftime('%b %-d %-I:%M %p')}

        self.assertEqual(message_dict, self.message.as_dict())
