from fastapi import APIRouter, Depends
from sqlalchemy import select, text, func
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.auth import get_current_user

router = APIRouter(tags=["Dashboard"])

def count_rows(db: Session, table: str):
    return db.scalar(text(f"SELECT COUNT(*) FROM {table}")) or 0

@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    return {
        "total_students": count_rows(db, "students"),
        "total_teachers": count_rows(db, "teachers"),
        "total_courses": count_rows(db, "courses"),
        "total_classes": count_rows(db, "class_rooms"),
        "open_classes": db.scalar(
            text("SELECT COUNT(*) FROM class_rooms WHERE status = 'OPEN'")
        ) or 0,
        "total_registrations": count_rows(db, "registrations"),
        "average_score": round(
            db.scalar(select(func.avg(models.Result.score))) or 0, 2
        )
    }