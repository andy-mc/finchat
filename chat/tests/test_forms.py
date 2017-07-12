from chat.factories import UserFactory
from chat.forms import UserCreationForm
from django.test import TestCase


class UserCreationFormTest(TestCase):

    def test_no_username(self):
        form = UserCreationForm(data={
            'email': 'test@gmail.com',
            'password1': 'test',
            'password2': 'test',
        })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('username'))

    def test_empty_passwords(self):
        form = UserCreationForm(data={
            'email': 'test@gmail.com',
            'username': 'test',
        })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('password1'))
        self.assertTrue(form.has_error('password2'))

    def test_passwords_not_match(self):
        form = UserCreationForm(data={
            'email': 'test@gmail.com',
            'username': 'test',
            'password1': "you'll never guess",
            'password2': "you'll never",
        })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('password2'))

    def test_user_creation_form_works(self):
        form = UserCreationForm(data={
            'email': 'test@gmail.com',
            'username': 'test',
            'password1': "you'll never guess",
            'password2': "you'll never guess",
        })

        self.assertTrue(form.is_valid())
