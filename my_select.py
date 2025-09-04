from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, desc, and_, cast, Numeric
from database import engine
from models import Group, Student, Teacher, Subject, Grade

# Створюємо сесію
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    """
    Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    """
    result = session.query(
        Student.fullname,
        cast(func.avg(Grade.grade), Numeric(10, 2)).label('avg_grade')
    ).join(Grade).group_by(Student.id, Student.fullname).order_by(desc('avg_grade')).limit(5).all()
    
    return result

def select_2(subject_name="Програмування"):
    """
    Знайти студента із найвищим середнім балом з певного предмета.
    """
    result = session.query(
        Student.fullname,
        Subject.name,
        cast(func.avg(Grade.grade), Numeric(10, 2)).label('avg_grade')
    ).select_from(Student).join(Grade).join(Subject).filter(
        Subject.name == subject_name
    ).group_by(Student.id, Student.fullname, Subject.name).order_by(desc('avg_grade')).first()
    
    return result

def select_3(subject_name="Математика"):
    """
    Знайти середній бал у групах з певного предмета.
    """
    result = session.query(
        Group.name,
        Subject.name,
        cast(func.avg(Grade.grade), Numeric(10, 2)).label('avg_grade')
    ).select_from(Grade).join(Student).join(Group).join(Subject).filter(
        Subject.name == subject_name
    ).group_by(Group.name, Subject.name).all()
    
    return result

def select_4():
    """
    Знайти середній бал на потоці (по всій таблиці оцінок).
    """
    result = session.query(
        cast(func.avg(Grade.grade), Numeric(10, 2)).label('avg_grade')
    ).scalar()
    
    return result

def select_5(teacher_name=None):
    """
    Знайти які курси читає певний викладач.
    """
    query = session.query(Teacher.fullname, Subject.name).join(Subject)
    
    if teacher_name:
        query = query.filter(Teacher.fullname.like(f"%{teacher_name}%"))
    
    result = query.all()
    return result

def select_6(group_name="IT-21"):
    """
    Знайти список студентів у певній групі.
    """
    result = session.query(
        Student.fullname, 
        Group.name
    ).join(Group).filter(Group.name == group_name).all()
    
    return result

def select_7(group_name="IT-21", subject_name="Програмування"):
    """
    Знайти оцінки студентів у окремій групі з певного предмета.
    """
    result = session.query(
        Student.fullname,
        Grade.grade,
        Grade.date_received,
        Subject.name,
        Group.name
    ).select_from(Grade).join(Student).join(Group).join(Subject).filter(
        and_(Group.name == group_name, Subject.name == subject_name)
    ).order_by(desc(Grade.date_received)).all()
    
    return result

def select_8(teacher_name=None):
    """
    Знайти середній бал, який ставить певний викладач зі своїх предметів.
    """
    query = session.query(
        Teacher.fullname,
        cast(func.avg(Grade.grade), Numeric(10, 2)).label('avg_grade')
    ).select_from(Grade).join(Subject).join(Teacher)
    
    if teacher_name:
        query = query.filter(Teacher.fullname.like(f"%{teacher_name}%"))
    
    result = query.group_by(Teacher.fullname).all()
    return result

def select_9(student_name=None):
    """
    Знайти список курсів, які відвідує певний студент.
    """
    query = session.query(
        Student.fullname,
        Subject.name
    ).select_from(Student).join(Grade).join(Subject).distinct()
    
    if student_name:
        query = query.filter(Student.fullname.like(f"%{student_name}%"))
    
    result = query.all()
    return result

def select_10(student_name=None, teacher_name=None):
    """
    Список курсів, які певному студенту читає певний викладач.
    """
    query = session.query(
        Student.fullname,
        Teacher.fullname,
        Subject.name
    ).select_from(Student).join(Grade).join(Subject).join(Teacher).distinct()
    
    if student_name:
        query = query.filter(Student.fullname.like(f"%{student_name}%"))
    if teacher_name:
        query = query.filter(Teacher.fullname.like(f"%{teacher_name}%"))
    
    result = query.all()
    return result

# Функція для тестування всіх запитів
def test_all_selects():
    """
    Тестування всіх функцій select
    """
    print("=== Тестування всіх запитів ===\n")
    
    print("1. 5 студентів із найбільшим середнім балом:")
    for student in select_1():
        print(f"  {student.fullname}: {student.avg_grade}")
    print()
    
    print("2. Студент із найвищим середнім балом з Програмування:")
    result = select_2("Програмування")
    if result:
        print(f"  {result.fullname}: {result.avg_grade} з предмету {result.name}")
    print()
    
    print("3. Середній бал у групах з Математики:")
    for group in select_3("Математика"):
        print(f"  Група {group.name}: {group.avg_grade}")
    print()
    
    print("4. Середній бал на потоці:")
    print(f"  {select_4()}")
    print()
    
    print("5. Курси першого викладача:")
    teachers = select_5()
    if teachers:
        teacher = teachers[0][0]
        for t in select_5(teacher):
            print(f"  {t[0]} читає {t[1]}")
    print()
    
    print("6. Студенти групи IT-21:")
    for student in select_6("IT-21"):
        print(f"  {student.fullname}")
    print()
    
    print("7. Оцінки групи IT-21 з Програмування (перші 5):")
    for grade in select_7("IT-21", "Програмування")[:5]:
        print(f"  {grade.fullname}: {grade.grade} ({grade.date_received.strftime('%Y-%m-%d')})")
    print()
    
    print("8. Середні оцінки викладачів:")
    for teacher in select_8():
        print(f"  {teacher.fullname}: {teacher.avg_grade}")
    print()
    
    print("9. Курси першого студента:")
    students = session.query(Student.fullname).first()
    if students:
        for course in select_9(students.fullname):
            print(f"  {course.fullname} відвідує {course.name}")
    print()
    
    print("10. Курси студента від певного викладача:")
    for relation in select_10()[:5]:  # Перші 5 записів
        print(f"  {relation[0]} вивчає {relation[2]} у {relation[1]}")

if __name__ == "__main__":
    test_all_selects()