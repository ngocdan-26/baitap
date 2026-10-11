
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app import models, schemas
from app.services import registration
from app.auth import get_current_user, admin_only

router = APIRouter(
    prefix="/registrations",
    tags=["Registrations"]
)

@router.post("", response_model=schemas.RegistrationOut, status_code=201)
def create_registration(
    data: schemas.RegistrationIn,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    student = db.get(models.Student, data.student_id)
    classroom = db.get(models.ClassRoom, data.class_id)

    if not student:
        raise HTTPException(404, "Không tìm thấy học viên")

    if not classroom:
        raise HTTPException(404, "Không tìm thấy lớp học")

    if classroom.status != "OPEN":
        raise HTTPException(400, "Lớp không mở đăng ký")

    if classroom.start_date and classroom.start_date < date.today():
        raise HTTPException(400, "Lớp đã bắt đầu")

    if registration.find_registration(
        db, data.student_id, data.class_id
    ):
        raise HTTPException(400, "Học viên đã đăng ký lớp này")

    count = registration.count_active_registrations(
        db, data.class_id
    )

    if count >= classroom.capacity:
        raise HTTPException(400, "Lớp đã đủ số lượng")

    try:
        return registration.create_registration(db, data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Đăng ký bị trùng"
        ) from exc

@router.get("", response_model=list[schemas.RegistrationOut])
def list_registrations(
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    return registration.get_registrations(db)

@router.delete("/{registration_id}")
def delete_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    registrations = registration.get_registration(db, registration_id)
    if not registrations:
        raise HTTPException(404, "Không tìm thấy đăng ký")
    
    registration.delete_registration(db, registrations)
    return {"message": "Đã hủy đăng ký"}
