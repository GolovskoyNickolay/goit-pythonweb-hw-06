import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Завантажуємо змінні оточення
load_dotenv()

# Отримуємо URL бази даних
DATABASE_URL = os.getenv("DATABASE_URL")

# Створюємо engine для підключення
engine = create_engine(DATABASE_URL, echo=False)

# Створюємо фабрику сесій
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для моделей
Base = declarative_base()

def get_db():
    """Функція для отримання сесії БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()