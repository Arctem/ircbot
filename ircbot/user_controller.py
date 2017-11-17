from datetime import datetime

import ircbot.storage as db
from ircbot.models import Channel, User, Presence, Message, Server


@db.atomic
def get_or_create_server(remote_id, protocol, s=None):
    server = s.query(Server).filter_by(remote_id=remote_id, protocol=protocol).one_or_none()
    if not server:
        server = Server(remote_id=remote_id, protocol=protocol)
    s.add(server)
    return server


@db.atomic
def get_or_create_channel(remote_id, server, s=None):
    channel = s.query(Channel).filter_by(remote_id=remote_id, server=server).one_or_none()
    if not channel:
        channel = Channel(remote_id=remote_id, server=server)
    s.add(channel)
    return channel


@db.needs_session
def get_user(remote_id, server, s=None):
    user = s.query(User).filter_by(remote_id=remote_id, server=server).one_or_none()
    return user


@db.atomic
def get_or_create_user(remote_id, server, s=None):
    user = s.query(User).filter_by(remote_id=remote_id, server=server).one_or_none()
    if not user:
        user = User(remote_id=remote_id, server=server)
    s.add(user)
    return user


@db.atomic
def create_message(user, channel, msg, private, remote_id=None, s=None):
    msg = Message(speaker=user, channel=channel, message=msg, remote_id=remote_id, timestamp=datetime.now())
    if not private:
        s.add(msg)
    return msg


@db.needs_session
def get_last_message(channel, user=None, s=None):
    if user:
        return s.query(Message).filter_by(speaker=user, channel=channel).order_by(Message.timestamp.desc()).first()
    else:
        return s.query(Message).filter_by(channel=channel).order_by(Message.timestamp.desc()).first()


@db.needs_session
def add_user_to_channel(user, channel, s=None):
    presence = s.query(Presence).filter_by(user=user, channel=channel).one_or_none()
    if not presence:
        presence = Presence(user=user, channel=channel)
        s.add(presence)
    return presence


@db.needs_session
def remove_user_from_channel(user, channel, s=None):
    return s.query(Presence).filter_by(user=user, channel=channel).delete() > 0


@db.needs_session
def empty_channel(channel, s=None):
    return s.query(Presence).filter_by(channel=channel).delete()

# need a more generic way to do this


@db.atomic
def set_attribute(nick, attribute, value, s=None):
    user = get_user(nick, s=s)
    bool_value = to_bool(value)
    if attribute == 'bot':
        if bool_value:
            user.bot = True
        elif bool_value:
            user.bot = False
        else:
            return False
        return True
    elif attribute == 'admin':
        if bool_value:
            user.admin = True
        elif bool_value:
            user.admin = False
        else:
            return False
        return True


def to_bool(value):
    if value is True:
        return True
    elif value is False:
        return False
    elif value.lower() in ['true', '1', 't']:
        return True
    elif value.lower() in ['false', '0', 'f']:
        return False
