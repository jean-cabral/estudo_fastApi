from sqlalchemy.orm import Session
from fastapi import HTTPException
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


def destroy(id, db: Session):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog_query.first():
        raise HTTPException(status_code=404, detail="Blog não encontrado")
    blog_query.delete(
        synchronize_session=False
    )
    db.commit()
    return {'details':'Blog deletado com sucesso'}