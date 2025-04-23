from sqlalchemy.orm import Session
import bcrypt
from typing import List
from crezu import tables
from crezu import models


class UserManager:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_data: models.UserCreate) -> tables.User:
        # Проверяем, существует ли пользователь с таким именем или email
        db_user_by_username = self.session.query(tables.User).filter(
            tables.User.username == user_data.username).first()
        if db_user_by_username:
            raise ValueError("Username already registered")

        db_user_by_email = self.session.query(tables.User).filter(
            tables.User.email == user_data.email).first()
        if db_user_by_email:
            raise ValueError("Email already registered")

        # Хешируем пароль
        hashed_password = bcrypt.hashpw(
            user_data.password.encode('utf-8'), bcrypt.gensalt())

        # Создаем нового пользователя
        db_user = tables.User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password.decode('utf-8')
        )

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_user(self, user_id: int) -> tables.User:
        user = self.session.query(tables.User).filter(
            tables.User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        return user

    def get_users(self, skip: int = 0, limit: int = 100) -> List[tables.User]:
        return self.session.query(tables.User).offset(skip).limit(limit).all()
