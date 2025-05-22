from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
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
