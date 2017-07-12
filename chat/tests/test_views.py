from chat.factories import MessageFactory, UserFactory
from chat.models import Message
from chat.views import home
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase


class TestHome(TestCase):

    def setUp(self):
        self.user = UserFactory(username="user")

    def test_home_url(self):
        url = resolve('/')
        self.assertEqual(url.func, home)

    def test_home_template(self):
        self.client.login(username="user", password="test")
        response = self.client.get(reverse(home))
        self.assertTemplateUsed(response, 'index.html')

    def test_home_return_last_50_messages(self):
        # Create 60 messages in db
        MessageFactory.create_batch(60)

        self.client.login(username="user", password="test")
        response = self.client.get(reverse(home))
        home_messages = response.context['messages']
        db_messages = Message.objects.all()

        self.assertEqual(len(home_messages), 50)
        self.assertEqual(len(db_messages), 60)
        self.assertEqual(list(home_messages),
                         list(db_messages.order_by('timestamp')[:50]))
