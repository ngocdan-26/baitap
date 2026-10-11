
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Course


def get_courses(db: Session, search: str | None = None):
    query = select(Course)

    if search:
        query = query.where(
            Course.name.ilike(f"%{search}%")
        )

    return list(db.scalars(query.order_by(Course.id)))


def get_course(db: Session, course_id: int):
    return db.get(Course, course_id)


def create_course(db: Session, data):
    course = Course(**data.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def update_course(db: Session, course: Course, data):
    for key, value in data.model_dump().items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course: Course):
    db.delete(course)
    db.commit()
