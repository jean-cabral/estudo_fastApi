from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status
from .. import models, schemas


def get_all(db:Session):
    """
    Retorna todos os registros de Blog
    """
    blogs = db.query(models.Blog).all()
    return blogs


def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(id: int, db: Session):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog não encontrado"
        )
    blog_query.delete(
        synchronize_session=False
    )
    db.commit()
    return {'details':'Blog deletado com sucesso'}

def update(id: int, request: schemas.Blog, db: Session):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog não encontrado"
        )

    blog_query.update(
        request.model_dump(exclude_unset=True)
    )
    db.commit()
    return blog_query

def get_blog(id:int, response, db: Session):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog com o id {id} não está disponível'
        )
    return blog_query