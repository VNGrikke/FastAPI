from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timezone

from database.database import get_db
from schemas.student import StandardResponse, StudentCreate, StudentUpdate
from services.students import StudentService

router = APIRouter(prefix="/students", tags=["Students"])

def format_response(request: Request, status_code: int, message: str, data: any = None, error: str = None):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "path": request.url.path
    }

@router.get("", response_model=StandardResponse)
def get_students(
    request: Request,
    name: Optional[str] = None,
    code: Optional[str] = None,
    email: Optional[str] = None,
    class_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    students = StudentService.get_students(db, name, code, email, class_id)
    return format_response(request, 200, "Lấy danh sách thành công", data=students)

@router.get("/{student_id}", response_model=StandardResponse)
def get_student(request: Request, student_id: int, db: Session = Depends(get_db)):
    student = StudentService.get_student_by_id(db, student_id)
    return format_response(request, 200, "Lấy chi tiết thành công", data=student)

@router.post("", response_model=StandardResponse, status_code=201)
def create_student(request: Request, student: StudentCreate, db: Session = Depends(get_db)):
    new_student = StudentService.create_student(db, student)
    return format_response(request, 201, "Thêm sinh viên thành công", data=new_student)

@router.put("/{student_id}", response_model=StandardResponse)
def update_student(request: Request, student_id: int, student_data: StudentUpdate, db: Session = Depends(get_db)):
    updated_student = StudentService.update_student(db, student_id, student_data)
    return format_response(request, 200, "Cập nhật sinh viên thành công", data=updated_student)

@router.delete("/{student_id}", response_model=StandardResponse)
def delete_student(request: Request, student_id: int, db: Session = Depends(get_db)):
    StudentService.delete_student(db, student_id)
    return format_response(request, 200, "Xóa sinh viên thành công", data=None)