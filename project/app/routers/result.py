
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app import models, schemas
from app.services import result
from app.auth import get_current_user, admin_only

router = APIRouter(prefix="/results", tags=["Results"])


@router.post("", response_model=schemas.ResultOut, status_code=201)
def create_result(
    data: schemas.ResultIn,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    registration = db.get(models.Registration, data.registration_id)
    if not registration:
        raise HTTPException(404, "Không tìm thấy đăng ký")
    if registration.result:
        raise HTTPException(400, "Đăng ký đã có kết quả")
    try:
        return result.create_result(db, data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Kết quả đã tồn tại"
        ) from exc


@router.get("", response_model=list[schemas.ResultOut])
def list_results(
    db: Session = Depends(get_db),
    _=Depends(get_current_user)
):
    return result.get_results(db)

@router.put("/{result_id}", response_model=schemas.ResultOut)
def update_result(
    result_id: int,
    data: schemas.ResultIn,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    results = result.get_result(db, result_id)
    if not results:
        raise HTTPException(404, "Không tìm thấy kết quả")
    registration = db.get(
        models.Registration, data.registration_id
    )
    if not registration:
        raise HTTPException(404, "Không tìm thấy đăng ký")
    other = db.scalar(
        select(models.Result).where(
            models.Result.registration_id == data.registration_id,
            models.Result.id != result_id
        )
    )
    if other:
        raise HTTPException(
            400, "Đăng ký này đã có kết quả khác"
        )
    try:
        return result.update_result(db, results, data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Dữ liệu kết quả không hợp lệ"
        ) from exc

@router.delete("/{result_id}")
def delete_result(
    result_id: int,
    db: Session = Depends(get_db),
    _=Depends(admin_only)
):
    results = result.get_result(db, result_id)
    if not results:
        raise HTTPException(404, "Không tìm thấy kết quả")
    result.delete_result(db, results)
    return {"message": "Đã xóa kết quả"}
