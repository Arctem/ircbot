from datetime import datetime

import ircbot.storage as db
from ircbot.models import User, UserChannel, Message

@db.atomic
def get_user(nick, name=None, host=None, s=None):
    user = s.query(User).filter_by(nick=nick).one_or_none()
    if user:
        if name:
            user.name = name
        if host:
            user.hostname = host
    return user

@db.atomic
def get_or_create_user(nick, name=None, host=None, s=None):
    user = get_user(nick, name=name, host=host, s=s)
    if not user:
        user = User(nick=nick, name=name, hostname=host)
        s.add(user)
    return user

@db.atomic
def save_message(user, channel, msg, s=None):
    if channel[0] != '#':
        return
    msg = Message(speaker=user, channel=channel, message=msg, timestamp=datetime.now())
    s.add(msg)

@db.needs_session
def get_last_message(channel, nick=None, s=None):
    if nick:
        target = get_user(nick)
        return s.query(Message).filter_by(speaker=target, channel=channel).order_by(Message.timestamp.desc()).first()
    else:
        return s.query(Message).filter_by(channel=channel).order_by(Message.timestamp.desc()).first()

@db.needs_session
def add_user_to_channel(user, channel, s=None):
    user_channel = s.query(UserChannel).filter_by(user=user, channel=channel).one_or_none()
    if not user_channel:
        user_channel = UserChannel(user=user, channel=channel)
        s.add(user_channel)
    return user_channel

@db.needs_session
def remove_user_from_channel(user, channel, s=None):
    return s.query(UserChannel).filter_by(user=user, channel=channel).delete() > 0

@db.needs_session
def empty_channel(channel, s=None):
    return s.query(UserChannel).filter_by(channel=channel).delete()

#need a more generic way to do this
@db.atomic
def set_attribute(nick, attribute, value, s=None):
    user = get_user(nick, s=s)
    if attribute == 'bot':
        if value.lower() in ['true', '1', 't']:
            user.bot = True
        elif value.lower() in ['false', '0', 'f']:
            user.bot = False
        else:
            return False
        return True
    elif attribute == 'admin':
        if value.lower() in ['true', '1', 't']:
            user.admin = True
        elif value.lower() in ['false', '0', 'f']:
            user.admin = False
        else:
            return False
        return True
