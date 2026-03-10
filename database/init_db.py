from database import Base, engine

from models.Role import Role
from models.AppUser import AppUser

def init_db():
    Base.metadata.create_all(engine)