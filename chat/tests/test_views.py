from chat.factories import MessageFactory, UserFactory
from chat.models import Message
from chat.views import SignUpView, UserDetail, home
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase


class TestHome(TestCase):

    def setUp(self):
        '''
        Creates a user, check UserFactory to see the
        default values.
        '''
        self.user = UserFactory(username="user")

    def test_home_url(self):
        url = resolve('/')
        # url.func is the view binded to url
        self.assertEqual(url.func, home)

    def test_authentication_control(self):
        '''Checks only authenticated users can view the page'''
        response = self.client.get(reverse(home))
        self.assertEqual(response.status_code, 302)

        self.client.login(username="user", password="test")
        response = self.client.get(reverse(home))
        self.assertEqual(response.status_code, 200)

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


class TestUserDetail(TestCase):

    def setUp(self):
        self.user = UserFactory(username="user")

    def test_user_detail_url(self):
        url = resolve('/users/{}/'.format(self.user.pk))
        self.assertEqual(url.func.__name__, UserDetail.__name__)

    def test_authentication_control(self):
        '''Checks only authenticated users can view the page'''
        response = self.client.get(reverse('user-detail',
                                           kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)

        self.client.login(username="user", password="test")
        response = self.client.get(reverse('user-detail',
                                           kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)

    def test_user_detail_template(self):
        self.client.login(username="user", password="test")
        response = self.client.get(reverse('user-detail',
                                           kwargs={'pk': self.user.pk}))
        self.assertTemplateUsed(response, 'chat/user-detail.html')

    def test_user_detail_message_history(self):
        # Create 2 message for test
        MessageFactory.create_batch(2, user=self.user)
        # Create 4 messages for random test users
        MessageFactory.create_batch(4)

        self.client.login(username="user", password="test")
        response = self.client.get(reverse('user-detail',
                                           kwargs={'pk': self.user.pk}))

        response_messages = response.context['messages']
        db_messages = Message.objects.all()
        user_messages = db_messages.filter(user=self.user
                                           ).order_by('-timestamp')

        self.assertEqual(len(db_messages), 6)
        self.assertEqual(len(response_messages), 2)
        self.assertEqual(list(response_messages),
                         list(user_messages))


class TestSignUpView(TestCase):

    def test_signup_url(self):
        url = resolve('/accounts/signup/')
        self.assertEqual(url.func.__name__, SignUpView.__name__)

    def test_signup_template(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'chat/signup.html')
