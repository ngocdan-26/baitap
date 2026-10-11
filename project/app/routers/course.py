
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app import schemas
from app.services import course
from app.auth import get_current_user, admin_only

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("", response_model=schemas.CourseOut, status_code=201)
def create_course(
    data: schemas.CourseIn,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    try:
        return course.create_course(db, data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Tên khóa học đã tồn tại"
        ) from exc


@router.get("", response_model=list[schemas.CourseOut])
def list_courses(
    search: str | None = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    return course.get_courses(db, search)


@router.get("/{course_id}", response_model=schemas.CourseOut)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    courses = course.get_course(db, course_id)
    if not courses:
        raise HTTPException(404, "Không tìm thấy khóa học")
    return courses


@router.put("/{course_id}", response_model=schemas.CourseOut)
def update_course(
    course_id: int,
    data: schemas.CourseIn,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    courses = course.get_course(db, course_id)
    if not courses:
        raise HTTPException(404, "Không tìm thấy khóa học")
    try:
        return course.update_course(db, courses, data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Tên khóa học đã tồn tại"
        ) from exc


@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    courses = course.get_course(db, course_id)
    if not courses:
        raise HTTPException(404, "Không tìm thấy khóa học")
    if courses.classes:
        raise HTTPException(
            400, "Không thể xóa khóa học đang có lớp"
        )
    course.delete_course(db, courses)
    return {"message": "Đã xóa khóa học"}
