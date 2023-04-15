from pydantic import BaseModel



class JokesSchema(BaseModel):
    joke: str 

    class Config:
        orm_mode = True
