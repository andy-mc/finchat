from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    label = models.SlugField(unique=True)

    def __str__(self):
        return self.label


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    user = models.ForeignKey(User)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return '{username}: {message}  [{timestamp}]'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {'username': self.user.username, 'message': self.message,
                'timestamp': self.formatted_timestamp}
