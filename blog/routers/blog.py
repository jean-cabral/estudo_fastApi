from typing import List
from fastapi import APIRouter, status, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..services import blog


router = APIRouter(
    prefix='/blog',
    tags=["Blogs"]
)


get_db = database.get_db

@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ShowBlog]
)
def all(db: Session = Depends(get_db)):
    return blog.get_all(db)

@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ShowBlog,
)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = blog.create(request, db)

    return new_blog


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlog
)
def show(id:int, response:Response, db: Session = Depends(get_db)):
    blog_query = blog.show(id, db)
    return blog_query


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
def destroy(id:int, db: Session = Depends(get_db)):
    blog_query = blog.destroy(id, db)

    return blog_query


@router.put(
    '/{id}',
    status_code=status.HTTP_202_ACCEPTED,
)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog_query = blog.update(id, request, db)
    return blog_query

