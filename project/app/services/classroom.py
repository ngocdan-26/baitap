from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import ClassRoom


def get_classes(db: Session):
    return list(db.scalars(select(ClassRoom).order_by(ClassRoom.id)))

def get_class(db: Session, class_id: int):
    return db.get(ClassRoom, class_id)

def create_class(db: Session, data):
    classroom = ClassRoom(**data.model_dump())
    db.add(classroom)
    db.commit()
    db.refresh(classroom)
    return classroom

def update_class(db: Session, classroom: ClassRoom, data):
    for key, value in data.model_dump().items():
        setattr(classroom, key, value)
        
    db.commit()
    db.refresh(classroom)
    return classroom

def delete_class(db: Session, classroom: ClassRoom):
    db.delete(classroom)
    db.commit()
