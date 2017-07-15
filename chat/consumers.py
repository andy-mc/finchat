import json
import logging
import re

from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from django.contrib.auth.models import User

from finbot.utils import finbot
from .models import Message, Room


log = logging.getLogger(__name__)


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({'accept': True})

    try:
        prefix, label = message['path'].strip('/').split('/')
        if prefix != 'chat':
            log.debug('invalid web socket path=%s', message['path'])
            return
        room = Room.objects.get(label=label)
    except ValueError:
        log.debug('invalid web socket path=%s', message['path'])
        return
    except Room.DoesNotExist:
        log.debug('room does not exist label=%s', label)
        return

    log.debug('chat connect room=%s client=%s:%s',
              room.label, message['client'][0], message['client'][1])

    Group('chat-' + label,
          channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['username'] = message.user.username
    message.channel_session['room'] = room.label


@channel_session_user
def ws_receive(message):
    # Take the room label from channel_session saved when ws_connect
    # Check if there is a room_model corresponding to the label
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
    except KeyError:
        log.debug('no room in channel_session')
        return
    except Room.DoesNotExist:
        log.debug('recieved message, but room does not exist label=%s', label)
        return

    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json")
        return

    if set(data.keys()) != set(('message',)):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        message_received = data['message']

        # Could be better using a regex to identify all possibles commands
        if message_received.startswith('/stock=') or message_received.startswith('/day_range='):
            bot_message = finbot(message_received)

            Group('chat-'+label,
                  channel_layer=message.channel_layer).send({'text': json.dumps(bot_message)})

            return

        user = User.objects.get(username=message.channel_session['username'])
        user_message = room.messages.create(user=user,
                                            message=message_received)

        Group('chat-' + label,
              channel_layer=message.channel_layer).send({'text': json.dumps(user_message.as_dict())})


@channel_session_user
def ws_disconnect(message):
    label = message.channel_session['room']
    Group('chat-' + label,
          channel_layer=message.channel_layer).discard(message.reply_channel)
