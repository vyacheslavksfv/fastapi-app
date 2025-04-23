from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, create_engine
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import os

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    # В реальном приложении храним хеш, не пароль
    password = Column(String(255))
    created_at = Column(DateTime, default=func.now())

    posts = relationship("Post", back_populates="author",
                         cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="author", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_id = Column(Integer, ForeignKey("users.id"))

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")

# Функция для создания движка БД


def get_engine():
    # Используем SQLite вместо MySQL для работы в CodeSandbox
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///crezu/blog.db")
    return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Функция для создания всех таблиц в БД


def create_tables():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
