from sqlalchemy import Column, Boolean, Integer, DateTime, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref

from ircbot.storage import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nick = Column(String, unique=True)
    name = Column(String)
    hostname = Column(String)
    admin = Column(Boolean, default=False)
    bot = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey('users.id'))
    # owner = relationship('User', remote_side=[id])
    # aliases = relationship('User', back_populates='owner')
    aliases = relationship('User', backref=backref('owner', remote_side=[id]))

    messages = relationship('Message', back_populates='speaker')
    user_channels = relationship('UserChannel', back_populates='user')


class UserChannel(Base):
    __tablename__ = 'user_channel'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='user_channels')
    channel = Column(String)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    speaker_id = Column(Integer, ForeignKey('users.id'))
    speaker = relationship('User', back_populates='messages', lazy='joined')
    channel = Column(String)
    message = Column(String)
    timestamp = Column(DateTime)

    def __str__(self):
        return '{date} <{nick}> {msg}'.format(date=self.timestamp, nick=self.speaker.nick, msg=self.message)
