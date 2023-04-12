from sqlalchemy import Column, Integer, String
from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Item(Base):
    __tablename__ = "jokes"

    id = Column(Integer, primary_key=True, index=True)
    joke = Column(String, index=True)