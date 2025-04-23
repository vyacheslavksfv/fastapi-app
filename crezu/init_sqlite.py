import sqlite3
import os
import bcrypt

"""
Скрипт для инициализации SQLite базы данных с использованием чистого SQL.
"""

# Путь к файлу базы данных
DB_PATH = 'blog.db'

# SQL-схема для создания таблиц
CREATE_TABLES_SQL = """
-- Удаляем таблицы, если они существуют
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

-- Создаем таблицу пользователей
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создаем индексы для таблицы пользователей
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- Создаем таблицу постов
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Создаем индексы для таблицы постов
CREATE INDEX idx_posts_title ON posts(title);
CREATE INDEX idx_posts_author ON posts(author_id);

-- Создаем таблицу комментариев
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    post_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Создаем индексы для таблицы комментариев
CREATE INDEX idx_comments_post ON comments(post_id);
CREATE INDEX idx_comments_author ON comments(author_id);
"""


def create_schema():
    """Создание схемы базы данных с использованием чистого SQL"""
    # Удаляем существующую базу данных, если требуется пересоздать
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    # Подключаемся к базе данных (создаст новую, если она не существует)
    conn = sqlite3.connect(DB_PATH)

    try:
        # Выполняем SQL для создания таблиц
        conn.executescript(CREATE_TABLES_SQL)
        print("Схема базы данных успешно создана.")
    except Exception as e:
        print(f"Ошибка при создании схемы базы данных: {e}")
    finally:
        conn.close()


def seed_data():
    """Заполнение базы данных тестовыми данными с использованием SQL"""
    # Подключаемся к базе данных
    conn = sqlite3.connect(DB_PATH)

    try:
        # Создаем курсор для выполнения SQL-запросов
        cursor = conn.cursor()

        # Проверяем, есть ли уже данные в таблице пользователей
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] > 0:
            print("База данных уже содержит данные, пропускаем заполнение.")
            return

        # Хешируем пароль (password123) для всех тестовых пользователей
        hashed_password = bcrypt.hashpw('password123'.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Вставляем пользователей
        users_data = [
            ('admin', 'admin@example.com', hashed_password),
            ('john_doe', 'john@example.com', hashed_password),
            ('jane_smith', 'jane@example.com', hashed_password)
        ]

        cursor.executemany(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            users_data
        )

        # Получаем ID созданных пользователей
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        admin_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM users WHERE username = 'john_doe'")
        john_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM users WHERE username = 'jane_smith'")
        jane_id = cursor.fetchone()[0]

        # Вставляем посты
        posts_data = [
            ('Первый пост', 'Содержимое первого поста. Это тестовый контент для проверки функциональности блога.', admin_id),
            ('О FastAPI', 'FastAPI - это современный, быстрый (высокопроизводительный) веб-фреймворк для создания API с Python 3.6+, основанный на стандартных подсказках типов Python.', admin_id),
            ('Введение в SQLAlchemy', 'SQLAlchemy - это инструментарий SQL на Python и объектно-реляционный преобразователь (ORM), который предоставляет разработчикам полный набор хорошо известных шаблонов корпоративного уровня.', john_id),
            ('Работа с Pydantic', 'Pydantic - это библиотека валидации данных на Python, которая использует подсказки типов для валидации данных и выполнения управления ошибками.', john_id),
            ('Мысли вслух', 'Просто делюсь некоторыми мыслями и размышлениями о жизни, вселенной и вообще.', jane_id)
        ]

        cursor.executemany(
            "INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)",
            posts_data
        )

        # Получаем ID созданных постов
        cursor.execute("SELECT id FROM posts ORDER BY id")
        post_ids = cursor.fetchall()
        post1_id = post_ids[0][0]
        post2_id = post_ids[1][0]
        post3_id = post_ids[2][0]
        post4_id = post_ids[3][0]
        post5_id = post_ids[4][0]

        # Вставляем комментарии
        comments_data = [
            ('Отличный первый пост!', post1_id, john_id),
            ('Спасибо за информацию.', post1_id, jane_id),
            ('FastAPI - действительно крутой фреймворк!', post2_id, john_id),
            ('Полностью согласен, я тоже считаю его очень удобным.', post2_id, jane_id),
            ('Хорошее введение, но можно было рассказать подробнее о моделях.',
             post3_id, admin_id),
            ('Pydantic - одна из моих любимых библиотек!', post4_id, admin_id),
            ('Очень философский пост!', post5_id, admin_id),
            ('Интересные мысли, продолжай в том же духе.', post5_id, john_id)
        ]

        cursor.executemany(
            "INSERT INTO comments (content, post_id, author_id) VALUES (?, ?, ?)",
            comments_data
        )

        # Фиксируем изменения
        conn.commit()
        print("База данных успешно заполнена тестовыми данными.")

    except Exception as e:
        conn.rollback()
        print(f"Ошибка при заполнении базы данных: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    create_schema()
    seed_data()
    print("Инициализация базы данных успешно завершена!")
