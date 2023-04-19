from pydantic import BaseModel
from typing import Optional, Union
from uuid import UUID

class User(BaseModel):
    username: str
    full_name: str
    email: str

class UserInDB(User):
    uuid: Optional[UUID]
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None