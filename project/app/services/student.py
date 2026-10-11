
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.models import Student


def get_students(db: Session, search: str | None = None):
    query = select(Student)

    if search:
        keyword = f"%{search}%"
        query = query.where(
            or_(
                Student.full_name.ilike(keyword),
                Student.email.ilike(keyword)
            )
        )

    return list(db.scalars(query.order_by(Student.id)))


def get_student(db: Session, student_id: int):
    return db.get(Student, student_id)


def create_student(db: Session, data):
    student = Student(**data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(db: Session, student: Student, data):
    for key, value in data.model_dump().items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student


def delete_student(db: Session, student: Student):
    db.delete(student)
    db.commit()
