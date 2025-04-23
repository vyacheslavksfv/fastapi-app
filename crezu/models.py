from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# User Schemas


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Post Schemas


class PostBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=1)


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str] = Field(None, min_length=1)


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    post_id: int


class CommentRead(CommentBase):
    id: int
    post_id: int
    author_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostRead(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    comments: List[CommentRead] = []
    author: Optional[UserRead] = None

    class Config:
        orm_mode = True
