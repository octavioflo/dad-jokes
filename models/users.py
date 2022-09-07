from enum import Enum
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4


class Role(Enum):
    ADMIN = "admin"
    USER = "user"


class Users(BaseModel):
    id: Optional[UUID] == uuid4()
    first_name: str
    email: str
    role: Role
