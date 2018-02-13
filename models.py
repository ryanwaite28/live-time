import sys, os, psycopg2, string, random, json

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from sqlalchemy.sql import func

from chamber import uniqueValue



Base = declarative_base()

class Accounts(Base):
    __tablename__ = 'accounts'

    id                  = Column(Integer, primary_key = True)
    type                = Column(String, default = 'USER') # Either: USER, ARTIST, VENUE
    displayname         = Column(String(80), nullable = False, default = '')
    username            = Column(String(80), nullable = False, default = '')
    phone               = Column(String(80), nullable = False, default = '')
    email               = Column(String, nullable = False, unique = True, default = '')
    booking_email       = Column(String, nullable = False, unique = True, default = '')
    paypal_email        = Column(String, nullable = False, unique = True, default = '')
    password            = Column(String, nullable = False)
    icon                = Column(String, default = '/static/img/anon.png')
    link                = Column(String, default = '')
    bio                 = Column(String(250), default = '')

    facebook            = Column(String, default = '')
    twitter             = Column(String, default = '')
    youtube             = Column(String, default = '')
    instagram           = Column(String, default = '')
    soundcloud          = Column(String, default = '')
    snapchat            = Column(String, default = '')
    itunes              = Column(String, default = '')
    spotify             = Column(String, default = '')
    tidal               = Column(String, default = '')
    pandora             = Column(String, default = '')

    date_created        = Column(DateTime, server_default=func.now())
    last_loggedin       = Column(DateTime, server_default=func.now())
    last_loggedout      = Column(DateTime)
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,
            'type': self.type,
            'displayname': self.displayname,
            'username': self.username,
            'phone': self.phone,
            'email': self.email,
            'booking_email': self.booking_email,
            'paypal_email': self.paypal_email,
            'icon': self.icon,
            'link': self.link,
            'bio': self.bio,

            'facebook': self.facebook,
            'twitter': self.twitter,
            'youtube': self.youtube,
            'instagram': self.instagram,
            'soundcloud': self.soundcloud,
            'snapchat': self.snapchat,
            'itunes': self.itunes,
            'spotify': self.spotify,
            'tidal': self.tidal,
            'pandora': self.pandora,

            'date_created': str(self.date_created),
            'last_loggedin': str(self.last_loggedin),
            'last_loggedout': str(self.last_loggedout),
            'unique_value': self.unique_value
        }


class Featured(Base):
    __tablename__ = 'featured'

    id                  = Column(Integer, primary_key = True)
    account_id          = Column(Integer, ForeignKey('accounts.id'))
    account_rel         = relationship('Accounts', foreign_keys=[account_id])
    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,
            'account_id': self.account_id,
            'account_rel': self.account_rel.serialize,
            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }


class Follows(Base):
    __tablename__ = 'follows'

    id                  = Column(Integer, primary_key = True)
    account_id          = Column(Integer, ForeignKey('accounts.id'))
    account_rel         = relationship('Accounts', foreign_keys=[account_id])
    follows_id          = Column(Integer, ForeignKey('accounts.id'))
    follows_rel         = relationship('Accounts', foreign_keys=[follows_id])
    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,
            'account_id': self.account_id,
            'account_rel': self.account_rel.serialize,
            'follows_id': self.follows_id,
            'follows': self.follows_rel.serialize,
            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }


class Events(Base):
    __tablename__ = 'events'

    id                  = Column(Integer, primary_key = True)
    title               = Column(String, nullable = False, default = '')
    desc                = Column(String, nullable = False, default = '')
    location            = Column(String, nullable = False, default = '')
    icon                = Column(String, default = '/static/img/anon.png')
    host_id             = Column(Integer, ForeignKey('accounts.id'))
    host_rel            = relationship('Accounts', foreign_keys=[host_id])
    closed              = Column(Boolean, default = False)
    performers          = relationship('EventPerformers', cascade='delete, delete-orphan', backref="EventPerformers")
    requests            = relationship('EventRequests', cascade='delete, delete-orphan', backref="EventRequests")
    event_date_time     = Column(DateTime)
    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,
            'title': self.title,
            'desc': self.desc,
            'location': self.location,
            'icon': self.icon,
            'host_id': self.host_id,
            'host_rel': self.host_rel.serialize,
            'closed': self.closed,
            'performers': [p.serialize for p in performers],
            # 'requests': [r.serialize for r in requests],
            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }


class EventPerformers(Base):
    __tablename__ = 'event_performers'

    id                  = Column(Integer, primary_key = True)
    event_id            = Column(Integer, ForeignKey('events.id'))
    event_rel           = relationship('Events', foreign_keys=[event_id])
    performer_id        = Column(Integer, ForeignKey('accounts.id'))
    performer_rel       = relationship('Accounts', foreign_keys=[performer_id])
    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,
            'account_id': self.account_id,
            'account_rel': self.account_rel.serialize,
            'performer_id': self.performer_id,
            'performer_rel': self.performer_rel.serialize,
            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }


class EventRequests(Base):
    __tablename__ = 'event_requests'

    id                  = Column(Integer, primary_key = True)
    account_id          = Column(Integer, ForeignKey('accounts.id'))
    account_rel         = relationship('Accounts', foreign_keys=[account_id])
    event_id            = Column(Integer, ForeignKey('events.id'))
    event_rel           = relationship('Events', foreign_keys=[event_id])
    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,
            'account_id': self.account_id,
            'account_rel': self.account_rel.serialize,
            'event_id': self.event_id,
            'event_rel': self.event_rel.serialize,
            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }


class Notifications(Base):
    __tablename__ = 'notifications'

    id                  = Column(Integer, primary_key = True)
    account_id          = Column(Integer, ForeignKey('accounts.id'))
    account_rel         = relationship('Accounts', foreign_keys=[account_id])
    message             = Column(String, nullable = False)
    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,
            'account_id': self.account_id,
            'account_rel': self.account_rel.serialize,
            'message': self.message,
            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }



class ChatRooms(Base):
    __tablename__ = 'chat_rooms'

    id                  = Column(Integer, primary_key = True)
    title               = Column(String, nullable = False)
    owner_id            = Column(Integer, ForeignKey('accounts.id'))
    owner_rel           = relationship('Accounts', foreign_keys=[owner_id])
    members             = relationship('ChatRoomMembers', cascade='delete, delete-orphan', backref="ChatRoomMembers")
    # messages            = relationship('ChatRoomMessages', cascade='delete, delete-orphan', backref="ChatRoomMessages")
    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,
            'title': self.title,
            'owner_id': self.owner_id,
            'owner_rel': self.owner_rel.serialize,
            # 'members': [m.serialize for m in self.members],
            # 'messages': [m.serialize for m in self.messages],
            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }



class ChatRoomMembers(Base):
    __tablename__ = 'chat_room_members'

    id                  = Column(Integer, primary_key = True)
    chatroom_id         = Column(Integer, ForeignKey('chat_rooms.id'))
    chatroom_rel        = relationship('ChatRooms', foreign_keys=[chatroom_id])
    member_id           = Column(Integer, ForeignKey('accounts.id'))
    member_rel          = relationship('Accounts', foreign_keys=[member_id])
    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,
            'chatroom_id': self.chatroom_id,
            'chatroom_rel': self.chatroom_rel.serialize,
            'member_id': self.member_id,
            'member_rel': self.member_rel.serialize,
            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }


class ChatRoomMessages(Base):
    __tablename__ = 'chat_room_messages'

    id                  = Column(Integer, primary_key = True)
    chatroom_id         = Column(Integer, ForeignKey('chat_rooms.id'))
    chatroom_rel        = relationship('ChatRooms', foreign_keys=[chatroom_id])
    owner_id            = Column(Integer, ForeignKey('accounts.id'))
    owner_rel           = relationship('Accounts', foreign_keys=[owner_id])
    message             = Column(String, nullable = False)
    date_created        = Column(DateTime, server_default=func.now())
    unique_value        = Column(String, default = uniqueValue)

    @property
    def serialize(self):
         # Returns Data Object In Proper Format
        return {
            'id': self.id,
            'chatroom_id': self.chatroom_id,
            'chatroom_rel': self.chatroom_rel.serialize,
            'owner_id': self.owner_id,
            'owner_rel': self.owner_rel.serialize,
            'message': self.message,
            'date_created': str(self.date_created),
            'unique_value': self.unique_value
        }






engine = create_engine('sqlite:///database.db', echo=True) # DEV
# engine = create_engine('', echo=True) # PROD

Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
db_session = DBSession()
