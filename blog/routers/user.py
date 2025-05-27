from typing import List
from fastapi import APIRouter, status, Depends, Response
from .. import schemas, database, models


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
def create_user(request: schemas.User, db=Depends(get_db)):
    hashedPassword = hashing.Hash.encrypt(request.password)
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashedPassword
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ShowUser],
    
)
def all(db=Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowUser,
    
)
def show(id, response:Response, db=Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id).first()
    if not user_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} is not available'
        )
    return user_query

@router.put(
    '/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    
)
def update(id, request: schemas.User, db=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.update(
        request.model_dump(exclude_unset=True)
    )

    db.commit()
    return {'details':'Usuário atualizado com sucesso'}