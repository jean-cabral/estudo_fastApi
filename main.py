from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()


@app.get("/blog/")
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} blogs published from the db'}
    else:
        return {'data': f'{limit} blogs from the db'}


@app.get("/blog/unpublished")
def unpublished():
    return {'data': 'all unpublished blogs'}


@app.get("/blog/{id}")
def show(id: int):
    return {'data': id}


@app.get("/blog/{id}/comments")
def comments(id: int):
    return {'data': {1, 2}}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post("/blog")
def create_blog(blog: Blog):
    return {'data': f'Blog is create with title as {blog.title}'}
