from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crezu import models
from crezu.database import get_db
from crezu.managers import UserManager
from typing import List
router = APIRouter()


@router.post("/", response_model=models.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
    manager = UserManager(db)
    try:
        return manager.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=models.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    manager = UserManager(db)
    try:
        return manager.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[models.UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    manager = UserManager(db)
    return manager.get_users(skip, limit)
