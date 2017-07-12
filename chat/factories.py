import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Message


class UserFactory(factory.django.DjangoModelFactory):
    """
    Creates a user.
    """
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')
    password = make_password('test')


class MessageFactory(factory.django.DjangoModelFactory):
    """
    Creates a message from a user.
    """
    class Meta:
        model = Message

    user = factory.SubFactory(UserFactory)
    message = factory.Faker('text', max_nb_chars=140)
