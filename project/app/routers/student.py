
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app import schemas
from app.services import student
from app.auth import get_current_user, admin_only

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("", response_model=schemas.StudentOut, status_code=201)
def create_student(
    data: schemas.StudentIn,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    try:
        return student.create_student(db, data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email học viên đã tồn tại"
        ) from exc

@router.get("", response_model=list[schemas.StudentOut])
def list_students(
    search: str | None = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    return student.get_students(db, search)


@router.get("/{student_id}", response_model=schemas.StudentOut)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    students = student.get_student(db, student_id)

    if not students:
        raise HTTPException(404, "Không tìm thấy học viên")

    return students


@router.put("/{student_id}", response_model=schemas.StudentOut)
def update_student(
    student_id: int,
    data: schemas.StudentIn,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    students = student.get_student(db, student_id)

    if not students:
        raise HTTPException(404, "Không tìm thấy học viên")

    try:
        return student.update_student(db, students, data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email học viên đã tồn tại"
        ) from exc


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    students = student.get_student(db, student_id)

    if not students:
        raise HTTPException(404, "Không tìm thấy học viên")

    try:
        student.delete_student(db, students)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Không thể xóa học viên đang có dữ liệu liên quan"
        ) from exc

    return {"message": "Đã xóa học viên"}
