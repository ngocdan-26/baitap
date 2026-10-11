
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.models import Teacher


def get_teachers(db: Session, search: str | None = None):
    query = select(Teacher)

    if search:
        keyword = f"%{search}%"
        query = query.where(
            or_(
                Teacher.full_name.ilike(keyword),
                Teacher.email.ilike(keyword)
            )
        )

    return list(db.scalars(query.order_by(Teacher.id)))


def get_teacher(db: Session, teacher_id: int):
    return db.get(Teacher, teacher_id)


def create_teacher(db: Session, data):
    teacher = Teacher(**data.model_dump())
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher


def update_teacher(db: Session, teacher: Teacher, data):
    for key, value in data.model_dump().items():
        setattr(teacher, key, value)

    db.commit()
    db.refresh(teacher)
    return teacher


def delete_teacher(db: Session, teacher: Teacher):
    db.delete(teacher)
    db.commit()
