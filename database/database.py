from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# TODO: make this the first set of jokes that get added.
# db: list[JokesSchema] = [ # https://www.countryliving.com/life/a27452412/best-dad-jokes/
#     JokesSchema(id=1, joke="I'm afraid for the calendar. Its days are numbered."),
#     JokesSchema(id=2, joke="What do you call a fish wearing a bowtie? Sofishticated."),
#     JokesSchema(id=3, joke="My wife said I should do lunges to stay in shape. That would be a big step forward."),
#     JokesSchema(id=4, joke="Singing in the shower is fun until you get soap in your mouth. Then it's a soap opera."),
# ]