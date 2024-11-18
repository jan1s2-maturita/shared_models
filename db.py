from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    is_admin = Column(Boolean)

    user_flags = relationship('UserFlag', back_populates='user')


# CTF Flags
class Flag(Base):
    __tablename__ = 'flags'
    id = Column(Integer, primary_key=True)
    flag = Column(String)
    description = Column(String)
    hint = Column(String)
    challenge_id = Column(Integer, ForeignKey('challenges.id'))
    challenge = relationship('Challenge', back_populates='flags')
    users = relationship('User', secondary='user_flags')

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    # k8s image manifest in JSON
    manifest = Column(JSON)
    description = Column(String)
    challenge_id = Column(Integer, ForeignKey('challenges.id'))
    challenge = relationship('Challenge', back_populates='image')

class Challenge(Base):
    __tablename__ = 'challenges'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category = Column(String)
    points = Column(Integer)
    flags = relationship('Flag', back_populates='challenge')
    image = relationship('Image', back_populates='challenge')
    users = relationship('User', secondary='user_flags')
# join table between completed flags and users
class UserFlag(Base):
    __tablename__ = 'user_flags'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    flag_id = Column(Integer, ForeignKey('flags.id'))
    challenge_id = Column(Integer, ForeignKey('challenges.id'))
    user = relationship('User', back_populates='user_flags')
    flag = relationship('Flag', back_populates='users')
    challenge = relationship('Challenge', back_populates='users')

