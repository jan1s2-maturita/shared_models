from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    admin = Column(Integer)

    def __init__(self, name, fullname, password, admin=False):
        self.name = name
        self.fullname = fullname
        self.password = password
        self.admin = admin

    def __repr__(self):
       return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)
# k8s pods
class Manifests(Base):
    __tablename__ = 'manifests'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    manifest = Column(String)
    admin_only = Column(Integer)

    def __init__(self, name, description, manifest, admin_only=False):
        self.name = name
        self.description = description
        self.manifest = manifest
        self.admin_only = admin_only

    def __repr__(self):
       return "<Manifests('%s','%s', '%s')>" % (self.name, self.description, self.manifest)

# ctf flags for the k8s pods
class Flags(Base):
    __tablename__ = 'flags'

    id = Column(Integer, primary_key=True)
    flag = Column(String)
    pod_id = Column(Integer, ForeignKey('manifests.id'))

    def __init__(self, flag, pod_id):
        self.flag = flag
        self.pod_id = pod_id

    def __repr__(self):
       return "<Flags('%s','%s')>" % (self.flag, self.pod_id)
