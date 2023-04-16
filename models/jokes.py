from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from schemas.jokes import JokesSchema

from database.database import Base


class JokesModel(Base):
    __tablename__ = "jokes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    joke = Column(String)

    def __init__(self, joke) -> None:
        self.joke = joke


    @classmethod
    def db_joke_by_id(cls, db: Session, joke_id: int):
        return db.query(cls).filter(cls.id == joke_id).first()

    @classmethod
    def db_insert_joke(cls, db: Session, new_joke: JokesSchema):
        joke = cls(new_joke.joke)
        db.add(joke)
        db.commit()

    @classmethod    
    def get_jokes(cls, db: Session, skip: int = 0, limit: int = 10):
        return db.query(cls).offset(skip).limit(limit).all()
    
    @classmethod
    def update_joke(cls, joke_id: int, new_joke: JokesSchema, db: Session):
        #db.update(cls).values({"column_name":"value"})
        db.query(cls).filter(cls.id == joke_id).update({"joke": new_joke.joke})
        db.commit()
    
    @classmethod
    def get_number_of_rows(cls, db: Session) -> int:
        return db.query(cls).count()
    