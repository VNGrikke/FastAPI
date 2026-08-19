from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.database import getdb
from ..services.student import get_all_student, create_student_service, get_student_with_courses
from ..schemas.student import StudentCreateReq, BaseResponseStudentDetail

router_student = APIRouter(
    prefix="/students",
    tags=["Student"]
)

@router_student.get("/")
def get_students(db: Session= Depends(getdb)):
    return {
        "message" : "Lay danh sach thanh cong",
        "data" : get_all_student(db)
    }

@router_student.post("/")
def create_student(data: StudentCreateReq, db: Session= Depends(getdb)):
    return  {
        "message" : "Them moi thanh cong",
        "data" : create_student_service(data, db)
    }

@router_student.get("/{id}/courses", response_model=BaseResponseStudentDetail)
def get_detail_student(id: int, db: Session= Depends(getdb)):
    return  {
        "message" : "Lay chi tiet thanh cong",
        "data" : get_student_with_courses(id, db)
    }