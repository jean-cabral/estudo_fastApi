from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

    blogs: Mapped[List["Blog"]] = relationship("Blog", back_populates="creator")


class Blog(Base):
    __tablename__ = "blog"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    body: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    creator: Mapped[User] = relationship("User", back_populates="blogs")
