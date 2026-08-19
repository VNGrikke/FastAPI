from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.student import StudentCreateReq
from services.student import create_student_service, get_all_students_service, get_student_with_workshops

router_student = APIRouter(prefix="/students", tags=["Student"])

@router_student.post("/")
def create_student(data: StudentCreateReq, db: Session = Depends(get_db)):
    return {"message": "Tạo sinh viên thành công", "data": create_student_service(data, db)}

@router_student.get("/")
def get_students(db: Session = Depends(get_db)):
    return {"message": "Lấy danh sách sinh viên thành công", "data": get_all_students_service(db)}

@router_student.get("/{id}/workshops")
def get_workshops_of_student(id: int, db: Session = Depends(get_db)):
    return {"message": "Lấy danh sách workshop của sinh viên thành công", "data": get_student_with_workshops(id, db)}