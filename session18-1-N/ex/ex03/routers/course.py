from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.database import getdb
from ..services.course import get_all_course, create_course_service
from ..schemas.course import CourseCreateReq

router_course = APIRouter(
    prefix="/courses",
    tags=["Course"]
)

@router_course.get("/")
def get_courses(db: Session = Depends(getdb)):
    return {
        "message": "Lay danh sach khoa hoc thanh cong",
        "data": get_all_course(db)
    }

@router_course.post("/")
def create_course(data: CourseCreateReq, db: Session = Depends(getdb)):
    return {
        "message": "Them moi khoa hoc thanh cong",
        "data": create_course_service(data, db)
    }

