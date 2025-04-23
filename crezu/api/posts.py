from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from crezu import models
from crezu.database import get_db
from crezu.managers import PostManager
from typing import List
router = APIRouter()


@router.post("/", response_model=models.PostRead, status_code=status.HTTP_201_CREATED)
def create_post(post: models.PostCreate, author_id: int, db: Session = Depends(get_db)):
    manager = PostManager(db)
    try:
        return manager.create_post(post, author_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[models.PostRead])
def read_posts(
    skip: int = 0,
    limit: int = 100,
    author_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    manager = PostManager(db)
    return manager.get_posts(skip, limit, author_id)


@router.get("/{post_id}", response_model=models.PostRead)
def read_post(post_id: int, db: Session = Depends(get_db)):
    manager = PostManager(db)
    try:
        return manager.get_post(post_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{post_id}", response_model=models.PostRead)
def update_post(post_id: int, post: models.PostUpdate, db: Session = Depends(get_db)):
    manager = PostManager(db)
    try:
        return manager.update_post(post_id, post)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    manager = PostManager(db)
    try:
        manager.delete_post(post_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return None
