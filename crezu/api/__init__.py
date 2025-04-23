from fastapi import APIRouter

from crezu.api import users, posts, comments
router = APIRouter()

# Подключаем все роутеры
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(posts.router, prefix="/posts", tags=["posts"])
router.include_router(comments.router, prefix="/comments", tags=["comments"])
