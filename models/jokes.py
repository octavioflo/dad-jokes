from uuid import UUID, uuid4
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4


class DadJokes(BaseModel):
    id: Optional[UUID]
    joke: str
