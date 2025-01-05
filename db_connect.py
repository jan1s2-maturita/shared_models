from .db import User, Challenge, Image, Flag, Service
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
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
        Service.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()
    def get_user_by_id(self, user_id):
        session = self.get_session()
        user = session.query(User).filter_by(id=user_id).first()
        session.close()
        return user
    def hash_password(self, password):
        from bcrypt import hashpw, gensalt
        return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
    def add_user(self, username, password, email):
        session = self.get_session()
        user = User(username=username, password=self.hash_password(password), email=email, is_admin=False)
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
    def get_service_manifest(self, challenge_id):
        session = self.get_session()
        image: Image = session.query(Image).filter_by(challenge_id=challenge_id).first()
        if not image:
            return None
        service = image.service
        session.close()
        return service.manifest

    def add_challenge(self, name, description, category):
        session = self.get_session()
        challenge = Challenge(name=name, description=description, category=category)
        session.add(challenge)
        id = challenge.id
        session.commit()
        session.close()
        return id
    def list_challenges(self):
        session = self.get_session()
        challenges = session.query(Challenge).all()
        session.close()
        return challenges
    def add_image(self, challenge_id, manifest):
        session = self.get_session()
        image = Image(challenge_id=challenge_id, manifest=manifest)
        session.add(image)
        id = image.id
        session.commit()
        session.close()
        return id
    def add_service(self, image_id, manifest):
        session = self.get_session()
        service = Service(image_id=image_id, manifest=manifest)
        session.add(service)
        session.commit()
        session.close()
    def add_flag(self, flag, challenge_id, points):
        session = self.get_session()
        flag_obj = Flag(flag=flag, challenge_id=challenge_id, points=points)
        session.add(flag_obj)
        id = flag_obj.id
        session.commit()
        session.close()
        return id
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
        res = [i.__dict__ for i in flags]
        session.close()
        return res
    def submit_user_flag(self, user_id, flag_id, submitted_flag):
        session = self.get_session()
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            session.close()
            return None
        flag = session.query(Flag).filter_by(id=flag_id).first()
        if not flag:
            session.close()
            return None
        if flag.flag == submitted_flag:
            user.flags.append(flag)
            session.commit()
            session.close()
            return user
        session.close()
        return None

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
    def update_user(self, user_id, password, is_admin):
        session = self.get_session()
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            session.close()
            return None
        if password:
            user.password = self.hash_password(password)
        if is_admin:
            user.is_admin = is_admin
        session.commit()
        session.close()
        return user
