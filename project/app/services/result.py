
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Result


def get_results(db: Session):
    return list(
        db.scalars(select(Result).order_by(Result.id))
    )

def get_result(db: Session, result_id: int):
    return db.get(Result, result_id)


def create_result(db: Session, data):
    result = Result(**data.model_dump())
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def update_result(db: Session, result: Result, data):
    for key, value in data.model_dump().items():
        setattr(result, key, value)

    db.commit()
    db.refresh(result)
    return result


def delete_result(db: Session, result: Result):
    db.delete(result)
    db.commit()
