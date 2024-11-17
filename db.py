from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    group_id = Column(Integer, ForeignKey('groups.id'))
    
    group = relationship('Group', back_populates='users')

    user_flags = relationship('UserFlag', back_populates='user')

class GroupPermission(Base):
    __tablename__ = 'group_permissions'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer)
    permission_id = Column(Integer)

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    groups = relationship('Group', secondary='group_permissions')

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)
    description = Column(String)
    permissions = relationship('Permission', secondary='group_permissions')
    users = relationship('User', back_populates='group')

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

