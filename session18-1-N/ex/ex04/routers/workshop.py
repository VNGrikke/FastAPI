from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.database import get_db
from services.workshop import get_workshop_with_students, register_student_to_workshop

router_workshop = APIRouter(prefix="/workshops", tags=["Workshop"])
router_registration = APIRouter(prefix="/registrations", tags=["Registration"])

@router_workshop.get("/{id}/students")
def get_students_of_workshop(id: int, db: Session = Depends(get_db)):
    return {"message": "Lấy danh sách sinh viên thành công", "data": get_workshop_with_students(id, db)}

class RegRequest(BaseModel):
    student_id: int
    workshop_id: int

@router_registration.post("/")
def create_registration(data: RegRequest, db: Session = Depends(get_db)):
    result = register_student_to_workshop(data.student_id, data.workshop_id, db)
    return {"message": "Đăng ký thành công", "data": result}