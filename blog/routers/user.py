from typing import List
from fastapi import APIRouter, status, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..services import user


router = APIRouter(
    prefix='/user',
    tags=["Users"]
)


get_db = database.get_db


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowUser,
    
)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ShowUser],
    
)
def all(db=Depends(get_db)):
    return user.get_all(db)


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowUser,
    
)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    return user.show(id, response, db)

@router.put(
    '/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    
)
def update(id: int, request: schemas.User, db: Session = Depends(get_db)):
    
    return user.update(id, request, db)