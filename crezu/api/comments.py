from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crezu import models
from crezu.database import get_db
from crezu.managers import CommentManager
from typing import List

router = APIRouter()


@router.post("/", response_model=models.CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(comment: models.CommentCreate, author_id: int, db: Session = Depends(get_db)):
    manager = CommentManager(db)
    try:
        return manager.create_comment(comment, author_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{comment_id}", response_model=models.CommentRead)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    manager = CommentManager(db)
    try:
        return manager.get_comment(comment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/post/{post_id}", response_model=List[models.CommentRead])
def read_comments_by_post(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    manager = CommentManager(db)
    try:
        return manager.get_comments_by_post(post_id, skip, limit)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    manager = CommentManager(db)
    try:
        manager.delete_comment(comment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None
