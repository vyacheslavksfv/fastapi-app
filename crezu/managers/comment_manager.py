from sqlalchemy.orm import Session
from typing import List

from crezu import tables
from crezu import models


class CommentManager:
    def __init__(self, session: Session):
        self.session = session

    def create_comment(self, comment_data: models.CommentCreate, author_id: int) -> tables.Comment:
        # Проверяем, существует ли пост
        post = self.session.query(tables.Post).filter(
            tables.Post.id == comment_data.post_id).first()
        if not post:
            raise ValueError("Post not found")

        # Проверяем, существует ли автор
        author = self.session.query(tables.User).filter(
            tables.User.id == author_id).first()
        if not author:
            raise ValueError("Author not found")

        # Создаем новый комментарий
        db_comment = tables.Comment(
            content=comment_data.content,
            post_id=comment_data.post_id,
            author_id=author_id
        )

        self.session.add(db_comment)
        self.session.commit()
        self.session.refresh(db_comment)
        return db_comment

    def get_comment(self, comment_id: int) -> tables.Comment:
        print(self.session.execute(
            """SELECT name FROM sqlite_master WHERE type='table';""").fetchall())
        comment = self.session.query(tables.Comment).filter(
            tables.Comment.id == comment_id).first()

        if not comment:
            raise ValueError("Comment not found")

        return comment

    def get_comments_by_post(self, post_id: int, skip: int = 0, limit: int = 100) -> List[tables.Comment]:
        # Проверяем, существует ли пост
        post = self.session.query(tables.Post).filter(
            tables.Post.id == post_id).first()
        if not post:
            raise ValueError("Post not found")

        comments = self.session.query(tables.Comment).filter(
            tables.Comment.post_id == post_id
        ).offset(skip).limit(limit).all()

        return comments

    def delete_comment(self, comment_id: int) -> None:
        comment = self.session.query(tables.Comment).filter(
            tables.Comment.id == comment_id).first()

        if not comment:
            raise ValueError("Comment not found")

        self.session.delete(comment)
        self.session.commit()
