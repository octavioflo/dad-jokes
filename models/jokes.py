from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, Session
from schemas.jokes import JokesSchema


from database.database import Base

def db_joke_by_id(db: Session, joke_id: int):
    return db.query(JokesModel).filter(JokesModel.id == joke_id).first()

def db_insert_joke(db: Session, new_joke: JokesSchema):
    # print(new_joke.joke)
    joke = JokesModel(new_joke.joke)
    #db.execute(JokesModel.insert(),new_joke)
    db.add(joke)
    db.commit()
    # db.refresh(new_joke.joke)


class JokesModel(Base):
    __tablename__ = "jokes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    joke = Column(String)

    def __init__(self, joke) -> None:
        self.joke = joke


    # @classmethod
    # def get_joke_by_id(cls, db: Session, joke_id: int):
    #     return db.query(cls).filter(cls.id == joke_id).first()

    # @classmethod
    # def insert_joke(cls, db: Session, new_joke: JokesSchema):
    #     #joke = JokesSchema(new_joke.joke)
    #     db.add(new_joke.joke)
    #     db.commit()
        #db.refresh(joke)
        
    # def get_user_by_email(cls, db: Session, email: str):
    #     return db.query(models.User).filter(models.User.email == email).first()


    # def get_users(self, db: Session, skip: int = 0, limit: int = 100):
    #     return db.query(models.User).offset(skip).limit(limit).all()
    