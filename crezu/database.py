from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from sqlalchemy.ext.declarative import declarative_base

from crezu.tables import get_engine

# Создаем фабрику сессий
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=get_engine())

# Функция-зависимость для получения сессии БД


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
