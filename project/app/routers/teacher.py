
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app import schemas
from app.services import teacher
from app.auth import get_current_user, admin_only

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.post("", response_model=schemas.TeacherOut, status_code=201)
def create_teacher(
    data: schemas.TeacherIn,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    try:
        return teacher.create_teacher(db, data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email giáo viên đã tồn tại"
        ) from exc

@router.get("", response_model=list[schemas.TeacherOut])
def list_teachers(
    search: str | None = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    return teacher.get_teachers(db, search)


@router.get("/{teacher_id}", response_model=schemas.TeacherOut)
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    teachers = teacher.get_teacher(db, teacher_id)
    if not teachers:
        raise HTTPException(404, "Không tìm thấy giáo viên")
    return teachers


@router.put("/{teacher_id}", response_model=schemas.TeacherOut)
def update_teacher(
    teacher_id: int,
    data: schemas.TeacherIn,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    teachers = teacher.get_teacher(db, teacher_id)
    if not teachers:
        raise HTTPException(404, "Không tìm thấy giáo viên")
    try:
        return teacher.update_teacher(db, teachers, data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email giáo viên đã tồn tại"
        ) from exc

@router.delete("/{teacher_id}")
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    teachers = teacher.get_teacher(db, teacher_id)
    if not teachers:
        raise HTTPException(404, "Không tìm thấy giáo viên")
    if teachers.classes:
        raise HTTPException(
            400, "Không thể xóa giáo viên đang phụ trách lớp"
        )
    teacher.delete_teacher(db, teachers)
    return {"message": "Đã xóa giáo viên"}
