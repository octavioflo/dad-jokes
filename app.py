from uuid import uuid4
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Path, Form, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from schemas.jokes import JokesSchema
from schemas.users import User, UserInDB, Token, TokenData
from typing import Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from botocore.exceptions import ClientError
from sqlalchemy.orm import Session
from database.database import SessionLocal, engine
from models.jokes import db_insert_joke, db_joke_by_id

import json
import boto3
import random
import models.jokes

models.jokes.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

# origins = [
#     "http://localhost",
#     "http://localhost:8080",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_secret(secret_name, region_name, secret_key):

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    # Decrypts secret using the associated KMS key.
    string_response = get_secret_value_response['SecretString']
    json_response = json.loads(string_response)
    return json_response[secret_key]


SECRET_KEY = get_secret("dev/dad-joke", "us-east-1", "dad-joke-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db: dict[User] = {
    "johndoe": {
        "uuid": uuid4(),
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", # it's secret
    },
    "alice": {
        "uuid": uuid4(),
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fake-secret2",
    },
}

db: list[JokesSchema] = [ # https://www.countryliving.com/life/a27452412/best-dad-jokes/
    JokesSchema(id=1, joke="I'm afraid for the calendar. Its days are numbered."),
    JokesSchema(id=2, joke="What do you call a fish wearing a bowtie? Sofishticated."),
    JokesSchema(id=3, joke="My wife said I should do lunges to stay in shape. That would be a big step forward."),
    JokesSchema(id=4, joke="Singing in the shower is fun until you get soap in your mouth. Then it's a soap opera."),
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    


@app.get("/")
async def root():
    return {"message": "Welcome to our Dad Jokes Application...."}


@app.get("/joke", response_model=JokesSchema, summary="Gets a dad joke", response_description="Returned dad joke.")
async def get_joke():
    '''
        Returns a dad joke directly from the super fancy database!
    '''
    return random.choice(db)


@app.post("/joke")
def create_joke(new_joke: JokesSchema, database: Session = Depends(get_db)):
    db_insert_joke(database, new_joke)
    return {"message": "success"}

@app.get("/joke/{id}", response_model=JokesSchema)  # https://fastapi.tiangolo.com/tutorial/path-params/
def get_joke_by_id(id: int = Path(title="The id of the joke.", ge=1), db: Session = Depends(get_db)):  # ge indicates the the number needs to be greater than or equal to 1, validation.
    joke = db_joke_by_id(db, id)
    if not joke:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Joke not found.")
    return joke
    


@app.put("/joke/{id}")
async def update_joke(id: int, new_joke: JokesSchema):
    for joke in db:
        if joke.id == id:
            joke.joke = new_joke.joke
            return {"message": "success"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Joke not found.")


@app.get("/jokes", response_model=list[JokesSchema])  # https://fastapi.tiangolo.com/tutorial/query-params/
async def get_jokes(skip: int = 0, limit: int = 10): #, token: str = Depends(oauth2_scheme)): if we want authentication
    return db[skip : skip + limit]



async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        raise credentials_exception from e
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post("/register")
async def create_user(user: UserInDB):
    user.hashed_password = get_password_hash(user.hashed_password)
    new_user = {user.username: user}  
    fake_users_db.update(new_user)
    return {"message": "success"}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/users/me', response_model=User)
async def get_user_data(current_user: User = Depends(get_current_user)):
    return current_user
