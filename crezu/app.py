from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

from crezu.api import router

app = FastAPI(title="Blog API",
              description="API для блога с постами и комментариями")

# Включаем CORS для работы в codesandbox.io
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware для логирования и замера времени выполнения запросов


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time

    # Логируем метод, путь и длительность
    print(f"{request.method} {request.url.path} completed in {duration:.3f}s")

    # Добавляем время выполнения в заголовок ответа
    response.headers["X-Process-Time"] = f"{duration:.3f}"

    return response

# Подключаем маршруты
app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в Blog API! Перейдите на /docs для документации."}
