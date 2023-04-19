from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, Session
from schemas.users import User, UserInDB
from uuid import uuid4
from database.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String)
    username = Column(String(50))
    full_name = Column(String(50))
    email = Column(String(50))
    hashed_password = Column(String)

    def __init__(
            self, 
            username: str, 
            full_name: str, 
            email: str, 
            hashed_password: str,
            uuid = uuid4(),
        ) -> None:
        self.uuid = str(uuid)
        self.username = username
        self.email = email
        self.full_name = full_name
        self.hashed_password = hashed_password
    
    
    @classmethod
    def create_user(cls, db: Session, user: UserInDB):
        new_user = cls(
            user.username, 
            user.full_name, 
            user.email, 
            user.hashed_password,
        )
        db.add(new_user)
        db.commit()
    
    @classmethod
    def get_user(cls, db: Session, username: str):
        user = db.query(cls).filter(cls.username == username).first()
        mapping = {
            "username": user.username, 
            "full_name": user.full_name, 
            "email": user.email, 
            "hashed_password": user.hashed_password
        }
        return UserInDB(**mapping)