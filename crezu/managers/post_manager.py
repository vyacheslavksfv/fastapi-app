from sqlalchemy.orm import Session, joinedload
from typing import Optional, List

from crezu import tables
from crezu import models


class PostManager:
    def __init__(self, session: Session):
        self.session = session

    def create_post(self, post_data: models.PostCreate, author_id: int) -> tables.Post:
        # Проверяем, существует ли автор
        author = self.session.query(tables.User).filter(
            tables.User.id == author_id).first()
        if not author:
            raise ValueError("Author not found")

        # Создаем новый пост
        db_post = tables.Post(**post_data.dict(), author_id=author_id)
        self.session.add(db_post)
        self.session.commit()
        self.session.refresh(db_post)
        return db_post

    def get_post(self, post_id: int) -> tables.Post:
        post = self.session.query(tables.Post).options(
            joinedload(tables.Post.author),
            joinedload(tables.Post.comments).joinedload(tables.Comment.author)
        ).filter(tables.Post.id == post_id).first()

        if not post:
            raise ValueError("Post not found")

        return post

    def get_posts(self, skip: int = 0, limit: int = 100, author_id: Optional[int] = None) -> List[tables.Post]:
        query = self.session.query(tables.Post)

        # Фильтрация по автору, если указан
        if author_id:
            query = query.filter(tables.Post.author_id == author_id)

        # Оптимизируем загрузку связанных данных
        query = query.options(
            joinedload(tables.Post.author),
            joinedload(tables.Post.comments).joinedload(tables.Comment.author)
        )

        posts = query.offset(skip).limit(limit).all()
        return posts

    def update_post(self, post_id: int, post_data: models.PostUpdate) -> tables.Post:
        post = self.session.query(tables.Post).filter(
            tables.Post.id == post_id).first()

        if not post:
            raise ValueError("Post not found")

        # Обновляем только предоставленные поля
        update_data = post_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(post, key, value)

        self.session.commit()
        self.session.refresh(post)
        return post

    def delete_post(self, post_id: int) -> None:
        post = self.session.query(tables.Post).filter(
            tables.Post.id == post_id).first()

        if not post:
            raise ValueError("Post not found")

        self.session.delete(post)
        self.session.commit()
