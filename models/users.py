from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, Session
from schemas.users import User, UserInDB

from database.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    full_name = Column(String(50))
    email = Column(String(50))
    hashed_password = Column(String)

    def __init__(
            self, 
            username: str, 
            full_name: str, 
            email: str, 
            password: str
        ) -> None:
        self.username = username
        self.email = email
        self.full_name = full_name
        self.password = password