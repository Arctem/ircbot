from datetime import datetime

import ircbot.storage as db
from ircbot.models import User, Message

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
