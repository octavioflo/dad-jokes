from uuid import uuid4
from fastapi import FastAPI, Query, Path
from models import DadJokes, Role
import random

app = FastAPI()

fake_users_db = [
    {
        "uuid": uuid4(),
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "role": Role.admin
    },
    {
        "uuid": uuid4(),
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "role": Role.user
    },
]

db: list[DadJokes] = [
    DadJokes(
        id=1, 
        joke="I'm afraid for the calendar. Its days are numbered."
    ),
    DadJokes(
        id=2, 
        joke="What do you call a fish wearing a bowtie? Sofishticated."
    ),
]


@app.get("/")
async def root():
    return {"Dad": "Jokes"}


@app.get("/joke")
async def get_joke():
    return random.choice(db)


@app.post("/joke")
async def create_joke(joke: DadJokes):
    db.append(joke)
    return {"message": "success"}


@app.get("/joke/{id}") # https://fastapi.tiangolo.com/tutorial/path-params/
async def get_joke_by_id(id: int = Path(title="The id of the joke.", ge=1)): #ge indicates the the number needs to be greater than or equal to 1, validation.
    for joke in db:
        if joke.id == id:
            return joke
    return {"error": "not found"}


@app.put("/joke/{id}")
async def update_joke(id: int, new_joke: DadJokes):
    for joke in db:
        if joke.id == id:
            joke.joke = new_joke.joke
            return {"message": "success"}
    return {"error": "not found"}


@app.get("/jokes") # https://fastapi.tiangolo.com/tutorial/query-params/
async def get_jokes(skip: int = 0, limit: int = 10):
    return db[skip : skip + limit]


@app.get("/roles/{role}")
async def get_role_description(role: Role):
    if role is Role.admin:
        return {"admin": "Administrator of the platform."}
    if role is Role.user:
        return {"user": "User of the application who is allowed to view Dad Jokes."}
