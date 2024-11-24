from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bcrypt import checkpw
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean)

    user_flags = relationship('UserFlag', back_populates='user')
    def verify_password(self, password: str) -> bool:
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
    description: Mapped[str] = mapped_column(String)
    hint: Mapped[str] = mapped_column(String)
    challenge_id: Mapped[int] = mapped_column(Integer, ForeignKey('challenges.id'))
    challenge = relationship('Challenge', back_populates='flags')
    users = relationship('User', secondary='user_flags')

class Image(Base):
    __tablename__ = 'images'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # k8s image manifest in JSON
    manifest: Mapped[dict] = mapped_column(JSON)
    description: Mapped[str] = mapped_column(String)
    challenge_id = mapped_column(Integer, ForeignKey('challenges.id'))
    challenge = relationship('Challenge', back_populates='image')

class Challenge(Base):
    __tablename__ = 'challenges'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    points: Mapped[int] = mapped_column(Integer)
    flags = relationship('Flag', back_populates='challenge')
    image = relationship('Image', back_populates='challenge')
    users = relationship('User', secondary='user_flags')
# join table between completed flags and users
class UserFlag(Base):
    __tablename__ = 'user_flags'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    flag_id: Mapped[int] = mapped_column(Integer, ForeignKey('flags.id'))
    challenge_id: Mapped[int] = mapped_column(Integer, ForeignKey('challenges.id'))
    user = relationship('User', back_populates='user_flags')
    flag = relationship('Flag', back_populates='users')
    challenge = relationship('Challenge', back_populates='users')

