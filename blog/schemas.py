from typing import List
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    model_config = {
        "from_attributes": True
    }


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog]
    model_config = {
        "from_attributes": True
    }

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
    model_config = {
        "from_attributes": True  # substitui orm_mode=True
    }
