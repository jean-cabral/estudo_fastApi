from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import models, schemas, hashing, docs
from .database import engine, get_db
from .routers import blog, user, authentication


app = FastAPI(openapi_tags=docs.tags_metadata)


models.Base.metadata.create_all(engine)


app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
