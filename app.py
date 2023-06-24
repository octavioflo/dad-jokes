from fastapi import FastAPI
from database.database import SessionLocal, engine
from api import jokes, users

import models.index

models.index.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(jokes.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Dad Jokes Application..."}

