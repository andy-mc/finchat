import json
import logging
import re

from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user
from django.contrib.auth.models import User

from finbot.utils import finbot
from .models import Message


log = logging.getLogger(__name__)


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({'accept': True})
    Group('finchat',
          channel_layer=message.channel_layer).add(message.reply_channel)
    message.channel_session['username'] = message.user.username


@channel_session_user
def ws_receive(message):
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
            
            Group('finchat',
              channel_layer=message.channel_layer).send({'text': json.dumps(bot_message)})
            
            return


        user = User.objects.get(username=message.channel_session['username'])
        user_message = Message.objects.create( user=user, 
                                               message=message_received)
        
        Group('finchat',
              channel_layer=message.channel_layer).send({'text': json.dumps(user_message.as_dict())})


@channel_session_user
def ws_disconnect(message):
    Group('finchat',
          channel_layer=message.channel_layer).discard(message.reply_channel)
