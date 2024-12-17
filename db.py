from typing import List, Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
Base = declarative_base()


user_flag_association = Table(
    'user_flag', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('flag_id', Integer, ForeignKey('flags.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean)

    flags = relationship('Flag', secondary=user_flag_association, back_populates='users')
    def verify_password(self, password: str) -> bool:
        from bcrypt import checkpw
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    def get_is_admin(self) -> bool:
        return self.is_admin
    def get_id(self) -> int:
        return self.id
    

    def __repr__(self):
        return f'<User {self.username}>'




# CTF Flags
class Flag(Base):
    __tablename__ = 'flags'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flag: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    hint: Mapped[str] = mapped_column(String, nullable=True)
    challenge_id = mapped_column(Integer, ForeignKey('challenges.id'))
    challenge = relationship('Challenge', back_populates='flags')
    users: Mapped[list["User"]] = relationship('User', back_populates='flags', secondary=user_flag_association)
    points: Mapped[int] = mapped_column(Integer)

class Service(Base):
    __tablename__ = 'services'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    manifest: Mapped[str] = mapped_column(String)
    image_id = mapped_column(Integer, ForeignKey('images.id'))
    image: Mapped["Image"] = relationship('Image', back_populates='service', uselist=False)

class Image(Base):
    __tablename__ = 'images'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # k8s image manifest in JSON
    manifest: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    challenge_id = mapped_column(Integer, ForeignKey('challenges.id'))
    challenge: Mapped["Challenge"] = relationship('Challenge', back_populates='image', uselist=False)
    service: Mapped["Service"] = relationship('Service', back_populates='image', uselist=False)

class Challenge(Base):
    __tablename__ = 'challenges'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String)
    flags: Mapped[list["Flag"]] = relationship('Flag', back_populates='challenge')
    image: Mapped["Image"] = relationship('Image', back_populates='challenge', uselist=False)
