from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./jokes.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# import sqlite3

# conn = sqlite3.connect('database/jokes.db')

# c = conn.cursor()

# c.execute("""CREATE TABLE jokes  (
#     id integer primary key autoincrement,
#     joke text
#     )""")

# c.execute("INSERT INTO jokes VALUES (1, 'Im afraid for the calendar. Its days are numbered.')")
# c.execute("INSERT INTO jokes VALUES (2, 'What do you call a fish wearing a bowtie? Sofishticated.')")
# c.execute("INSERT INTO jokes VALUES (3, 'My wife said I should do lunges to stay in shape. That would be a big step forward.')")
# c.execute("INSERT INTO jokes VALUES (4, 'Singing in the shower is fun until you get soap in your mouth. Then its a soap opera.')")

# # c.execute("SELECT * FROM jokes WHERE id=1")
# # result = c.fetchone()
# # print(result)
# conn.commit()
# conn.close()