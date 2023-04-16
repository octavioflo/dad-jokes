from fastapi import APIRouter, Path, HTTPException, Depends, status
from sqlalchemy.orm import Session
from schemas.index import JokesSchema
from models.index import JokesModel 
from dependencies import get_db
import random

router = APIRouter()


@router.get("/joke", response_model=JokesSchema, summary="Gets a dad joke", response_description="Returns a random dad joke.")
async def get_joke(database: Session = Depends(get_db)):
    '''
        Returns a dad joke directly from the super fancy database!
    '''
    rows = JokesModel.get_number_of_rows(database) # get the size of the database so we don't go out of range
    jid = random.randint(1, rows)
    return JokesModel.db_joke_by_id(database, jid)


@router.post("/joke")
def create_joke(new_joke: JokesSchema, database: Session = Depends(get_db)):
    JokesModel.db_insert_joke(database, new_joke)
    return {"message": "success"}


@router.get("/joke/{id}", response_model=JokesSchema)  # https://fastapi.tiangolo.com/tutorial/path-params/
def get_joke_by_id(id: int = Path(title="The id of the joke.", ge=1), database: Session = Depends(get_db)):  # ge indicates the the number needs to be greater than or equal to 1, validation.
    joke = JokesModel.db_joke_by_id(database, id)
    if not joke:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Joke not found.")
    return joke
    

@router.put("/joke/{id}")
async def update_joke(id: int, new_joke: JokesSchema, database: Session = Depends(get_db)):
    joke = JokesModel.db_joke_by_id(database, id)
    if not joke:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Joke not found.")
    JokesModel.update_joke(id, new_joke, database)
    return {"message": "success"}


@router.get("/jokes", response_model=list[JokesSchema])  # https://fastapi.tiangolo.com/tutorial/query-params/
async def get_jokes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)): #, token: str = Depends(oauth2_scheme)): if we want authentication
    return JokesModel.get_jokes(db, skip, limit)

