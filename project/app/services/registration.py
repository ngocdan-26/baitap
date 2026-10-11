from sqlalchemy import select, text
from sqlalchemy.orm import Session
from app.models import Registration


def get_registrations(db: Session):
    return list(db.scalars(
        select(Registration).order_by(Registration.id)
    ))

def get_registration(db: Session, registration_id: int):
    return db.get(Registration, registration_id)

def count_active_registrations(db: Session, class_id: int):
    return db.scalar(
        text("""
            SELECT COUNT(*)
            FROM registrations
            WHERE class_id = :class_id
              AND status = 'ACTIVE'
        """),
        {"class_id": class_id}
    ) or 0

def find_registration(db: Session, student_id: int, class_id: int):
    return db.scalar(
        select(Registration).where(
            Registration.student_id == student_id,
            Registration.class_id == class_id
        )
    )

def create_registration(db: Session, data):
    registration = Registration(**data.model_dump())
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration

def delete_registration(db: Session, registration: Registration):
    db.delete(registration)
    db.commit()