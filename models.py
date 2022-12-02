from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from enum import Enum


class Role(str, Enum):
    user = "user"
    admin = "admin"


class DadJokes(BaseModel):
    id: int
    joke: str


class User(BaseModel):
    id: Optional[UUID]
    username: str
    full_name: str
    email: str
    hashed_password: str
    role: Role
