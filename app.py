from uuid import uuid4
from fastapi import FastAPI
from models.jokes import DadJokes
import random


app = FastAPI()

db: list[DadJokes] = [
    DadJokes(id=uuid4(), joke="I'm afraid for the calendar. Its days are numbered."),
    DadJokes(
        id=uuid4(), joke="What do you call a fish wearing a bowtie?" "Sofishticated."
    ),
]


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/joke")
async def get_joke():
    return random.choice(db)
