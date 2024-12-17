from .db import User, Challenge, Image, Flag
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from bcrypt import hashpw, gensalt
# database connection class - postgres
class Database:
    def __init__(self, host, port, user, password, db_name):
        self.engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
        self.Session = sessionmaker(bind=self.engine)
        self.init_db()
    def init_db(self):
        Flag.metadata.create_all(self.engine)
        User.metadata.create_all(self.engine)
        Challenge.metadata.create_all(self.engine)
        Image.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()
    def get_user_by_id(self, user_id):
        session = self.get_session()
        user = session.query(User).filter_by(id=user_id).first()
        session.close()
        return user
    def add_user(self, username, password, email):
        session = self.get_session()
        user = User(username=username, password=hashpw(password.encode('utf-8'), gensalt()), email=email)
        session.add(user)
        session.commit()
        session.close()
        return user
    def get_user_by_username(self, username) -> User:
        session = self.get_session()
        user = session.query(User).filter_by(username=username).first()
        session.close()
        return user
    def get_user_by_creds(self, username, password) -> User|None:
        session = self.get_session()
        user = session.query(User).filter_by(username=username).first()
        if user and user.verify_password(password):
            return user
        return None
    def get_image_manifest(self, challenge_id):
        session = self.get_session()
        image: Image = session.query(Image).filter_by(challenge_id=challenge_id).first()
        if not image:
            return None
        session.close()
        return image.manifest
    def add_challenge(self, name, description, category):
        session = self.get_session()
        challenge = Challenge(name=name, description=description, category=category)
        session.add(challenge)
        session.commit()
        session.close()
        return challenge
    def list_challenges(self):
        session = self.get_session()
        challenges = session.query(Challenge).all()
        session.close()
        return challenges
    def add_image(self, challenge_id, manifest):
        session = self.get_session()
        image = Image(challenge_id=challenge_id, manifest=manifest)
        session.add(image)
        session.commit()
        session.close()
        return image
    def add_flag(self, flag, challenge_id, points):
        session = self.get_session()
        flag = Flag(flag=flag, challenge_id=challenge_id, points=points)
        session.add(flag)
        session.commit()
        session.close()
        return flag
    def get_challenge_by_id(self, challenge_id):
        session = self.get_session()
        challenge = session.query(Challenge).filter_by(id=challenge_id).first()
        session.close()
        return challenge
    def get_challenges(self):
        session = self.get_session()
        challenges = session.query(Challenge).all()
        session.close()
        return challenges
    def get_flags(self, challenge_id):
        session = self.get_session()
        flags = session.query(Flag).filter_by(challenge_id=challenge_id).all()
        session.close()
        return flags
    def submit_user_flag(self, user_id, flag_id):
        session = self.get_session()
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            session.close()
            return None
        flag = session.query(Flag).filter_by(id=flag_id).first()
        user.flags.append(flag)
        session.commit()
        session.close()
        return user
    def get_user_flags(self, user_id):
        session = self.get_session()
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            session.close()
            return None
        flags = user.flags
        session.close()
        return flags
    def get_flag_by_id(self, flag_id):
        session = self.get_session()
        flag = session.query(Flag).filter_by(id=flag_id).first()
        session.close()
        return flag
    def set_admin(self, user_id, admin):
        session = self.get_session()
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            session.close()
            return None
        user.is_admin = admin
        session.commit()
        session.close()
        return user


