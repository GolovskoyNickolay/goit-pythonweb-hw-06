from faker import Faker
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from database import engine
from models import Group, Student, Teacher, Subject, Grade

# Створюємо сесію
Session = sessionmaker(bind=engine)
session = Session()

# Ініціалізуємо Faker для генерації випадкових даних
fake = Faker('uk_UA')  # Українська локалізація

def create_groups():
    """Створення груп студентів"""
    groups = [
        Group(name='IT-21'),
        Group(name='CS-22'),
        Group(name='AI-23'),
    ]
    session.add_all(groups)
    session.commit()
    print("Створено 3 групи")
    return groups

def create_teachers():
    """Створення викладачів"""
    teachers = []
    for _ in range(5):  # Створюємо 5 викладачів
        teacher = Teacher(
            fullname=fake.name()
        )
        teachers.append(teacher)
    
    session.add_all(teachers)
    session.commit()
    print("Створено 5 викладачів")
    return teachers

def create_subjects(teachers):
    """Створення предметів"""
    subject_names = [
        'Математика',
        'Фізика', 
        'Програмування',
        'База даних',
        'Алгоритми',
        'Мережі',
        'Операційні системи',
        'Англійська мова'
    ]
    
    subjects = []
    for name in subject_names:
        subject = Subject(
            name=name,
            teacher_id=random.choice(teachers).id
        )
        subjects.append(subject)
    
    session.add_all(subjects)
    session.commit()
    print("Створено 8 предметів")
    return subjects

def create_students(groups):
    """Створення студентів"""
    students = []
    for _ in range(50):  # Створюємо 50 студентів
        student = Student(
            fullname=fake.name(),
            group_id=random.choice(groups).id
        )
        students.append(student)
    
    session.add_all(students)
    session.commit()
    print("Створено 50 студентів")
    return students

def create_grades(students, subjects):
    """Створення оцінок"""
    grades = []
    
    for student in students:
        # Кожен студент отримує від 10 до 20 оцінок
        num_grades = random.randint(10, 20)
        
        for _ in range(num_grades):
            grade = Grade(
                grade=round(random.uniform(1.0, 5.0), 1),  # Оцінка від 1.0 до 5.0
                date_received=fake.date_between(
                    start_date=datetime.now() - timedelta(days=365),
                    end_date=datetime.now()
                ),
                student_id=student.id,
                subject_id=random.choice(subjects).id
            )
            grades.append(grade)
    
    session.add_all(grades)
    session.commit()
    print(f"Створено {len(grades)} оцінок")

def seed_database():
    """Основна функція заповнення бази даних"""
    print("Початок заповнення бази даних...")
    
    try:
        # Очищення існуючих даних (якщо потрібно)
        session.query(Grade).delete()
        session.query(Student).delete()
        session.query(Subject).delete()
        session.query(Teacher).delete()
        session.query(Group).delete()
        session.commit()
        print("Очищено існуючі дані")
        
        # Створення даних
        groups = create_groups()
        teachers = create_teachers()
        subjects = create_subjects(teachers)
        students = create_students(groups)
        create_grades(students, subjects)
        
        print("База даних успішно заповнена!")
        
    except Exception as e:
        print(f"❌ Помилка: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()         