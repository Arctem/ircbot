from sqlalchemy import Column, Boolean, Integer, DateTime, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref

from ircbot.storage import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    remote_id = Column(String, unique=True)
    name = Column(String)
    admin = Column(Boolean, default=False)
    bot = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey('users.id'))
    # owner = relationship('User', remote_side=[id])
    # aliases = relationship('User', back_populates='owner')
    aliases = relationship('User', backref=backref('owner', remote_side=[id]))

    server_id = Column(Integer, ForeignKey('servers.id'))
    server = relationship('Server', back_populates='users')

    messages = relationship('Message', back_populates='speaker')
    presences = relationship('Presence', back_populates='player')


class Presence(Base):
    __tablename__ = 'presences'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('users.id'))
    player = relationship('User', back_populates='presences')
    channel_id = Column(Integer, ForeignKey('channels.id'))
    channel = relationship('Channel', back_populates='presences')


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    remote_id = Column(String, unique=True)
    speaker_id = Column(Integer, ForeignKey('users.id'))
    speaker = relationship('User', back_populates='messages', lazy='joined')
    channel_id = Column(Integer, ForeignKey('channels.id'))
    channel = relationship('Channel', back_populates='messages')

    message = Column(String)
    timestamp = Column(DateTime)

    def __str__(self):
        return '{date} <{name}> {msg}'.format(date=self.timestamp, name=self.speaker.name, msg=self.message)


class Server(Base):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True)
    remote_id = Column(String, unique=True)
    name = Column(String)
    protocol = Column(String)

    channels = relationship('Channel', back_populates='server')
    users = relationship('User', back_populates='server')


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)
    remote_id = Column(String, unique=True)
    name = Column(String)
    private = Column(Boolean)

    server_id = Column(Integer, ForeignKey('servers.id'))
    server = relationship('Server', back_populates='channels')

    presences = relationship('Presence', back_populates='channel')
    messages = relationship('Message', back_populates='channel')
