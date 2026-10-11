
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app import models, schemas
from app.services import classroom
from app.auth import get_current_user, admin_only

router = APIRouter(prefix="/classes", tags=["Classes"])

def validate_class(data, db):
    if not db.get(models.Course, data.course_id):
        raise HTTPException(400, "Khóa học không tồn tại")
    if not db.get(models.Teacher, data.teacher_id):
        raise HTTPException(400, "Giáo viên không tồn tại")
    if (
        data.start_date and data.end_date
        and data.end_date < data.start_date
    ):
        raise HTTPException(400, "Ngày kết thúc không hợp lệ")
    if data.status not in ["OPEN", "CLOSED", "FINISHED"]:
        raise HTTPException(400, "Trạng thái lớp không hợp lệ")


@router.post("", response_model=schemas.ClassOut, status_code=201)
def create_class(
    data: schemas.ClassIn,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    validate_class(data, db)

    try:
        return classroom.create_class(db, data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Tên lớp đã tồn tại"
        ) from exc


@router.get("", response_model=list[schemas.ClassOut])
def list_classes(
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    return classroom.get_classes(db)


@router.get("/{class_id}", response_model=schemas.ClassOut)
def get_class(
    class_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    classrooms = classroom.get_class(db, class_id)
    if not classrooms:
        raise HTTPException(404, "Không tìm thấy lớp học")
    return classrooms

@router.put("/{class_id}", response_model=schemas.ClassOut)
def update_class(
    class_id: int,
    data: schemas.ClassIn,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    classrooms = classroom.get_class(db, class_id)
    if not classrooms:
        raise HTTPException(404, "Không tìm thấy lớp học")
    validate_class(data, db)
    try:
        return classroom.update_class(db, classrooms, data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Tên lớp đã tồn tại"
        ) from exc

@router.delete("/{class_id}")
def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    classrooms = classroom.get_class(db, class_id)
    if not classrooms:
        raise HTTPException(404, "Không tìm thấy lớp học")
    if classrooms.registrations:
        raise HTTPException(
            400, "Không thể xóa lớp đã có đăng ký"
        )
    classroom.delete_class(db, classrooms)
    return {"message": "Đã xóa lớp học"}
