from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import models, schemas, hashing, docs
from .database import engine, SessionLocal


app = FastAPI(openapi_tags=docs.tags_metadata)

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog, tags=["Blogs"])
def create(request: schemas.Blog, db=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.get('/blog', status_code=status.HTTP_200_OK, tags=["Blogs"], response_model=List[schemas.ShowBlog])
def all(db=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, tags=["Blogs"], response_model=schemas.ShowBlog)
def show(id, response:Response, db=Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with the id {id} is not available'
        )
    return blog_query


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def destroy(id, db=Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog_query.first():
        raise HTTPException(status_code=404, detail="Blog não encontrado")
    blog_query.delete(
        synchronize_session=False
    )
    db.commit()
    return {'details':'Blog deletado com sucesso'}


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def update(id, request: schemas.Blog, db=Depends(get_db)):
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog_query.first():
        raise HTTPException(status_code=404, detail="Blog não encontrado")

    blog_query.update(
        request.model_dump(exclude_unset=True)
    )
    db.commit()
    return {'details':'Blog atualizado com sucesso'}


@app.post('/user',status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser, tags=["Users"])
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


@app.get('/user',status_code=status.HTTP_200_OK, response_model=List[schemas.ShowUser], tags=["Users"])
def all(db=Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get('/user/{id}',status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["Users"])
def show(id, response:Response, db=Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id).first()
    if not user_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id {id} is not available'
        )
    return user_query

@app.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["Users"])
def update(id, request: schemas.User, db=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user.update(
        request.model_dump(exclude_unset=True)
    )

    db.commit()
    return {'details':'Usuário atualizado com sucesso'}