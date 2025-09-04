import argparse
import sys
from sqlalchemy.orm import sessionmaker
from database import engine
from models import Group, Student, Teacher, Subject, Grade

# Створюємо сесію
Session = sessionmaker(bind=engine)
session = Session()

def main():
    """Головна функція CLI програми"""
    parser = argparse.ArgumentParser(description='University Database CLI')
    
    # Основні аргументи
    parser.add_argument('-a', '--action', 
                       choices=['create', 'list', 'update', 'remove'],
                       required=True,
                       help='CRUD операція')
    
    parser.add_argument('-m', '--model',
                       choices=['Teacher', 'Group', 'Student', 'Subject'],
                       required=True,
                       help='Модель для операції')
    
    # Допоміжні аргументи
    parser.add_argument('--id', type=int, help='ID запису для update/remove')
    parser.add_argument('--name', help='Ім\'я або назва')
    
    args = parser.parse_args()
    
    # Тут будуть функції для обробки команд
    print(f"Операція: {args.action}, Модель: {args.model}")

if __name__ == "__main__":
    main()