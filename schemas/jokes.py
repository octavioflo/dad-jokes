from pydantic import BaseModel



class JokesSchema(BaseModel):
    #id: int
    joke: str 

    class Config:
        orm_mode = True


