from sqlalchemy import Column, Integer, String, Enum as SAEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(SAEnum):
    ADMIN = "admin"
    GUARD = "guard"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default=Role.USER)
    firm_name = Column(String)
    full_name = Column(String)
