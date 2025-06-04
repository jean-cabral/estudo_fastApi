from typing import List
from fastapi import APIRouter, status, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..hashing import Hash

def create(request: schemas.User, db: Session):
    hashedPassword = Hash.encrypt(request.password)
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashedPassword
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all(db: Session):
    users = db.query(models.User).all()
    return users


def show(id: int, response: Response, db: Session):
    user_query = db.query(models.User).filter(models.User.id == id).first()
    if not user_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User com o id {id} não está disponível'
        )
    return user_query


def update(id:int, request: schemas.User, db: Session):
    user_query = db.query(models.User).filter(models.User.id == id)

    if not user_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    user_query.update(
        request.model_dump(exclude_unset=True)
    )

    db.commit()
    return user_query