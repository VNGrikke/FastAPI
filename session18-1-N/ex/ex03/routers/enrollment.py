from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.database import getdb
from ..services.enrollment import get_all_enrollment, create_enrollment_service
from ..schemas.enrollment import EnrollmentCreateReq

router_enrollment = APIRouter(
    prefix="/enrollments",
    tags=["Enrollment"]
)

@router_enrollment.get("/")
def get_enrollments(db: Session = Depends(getdb)):
    return {
        "message": "Lay danh sach dang ky thanh cong",
        "data": get_all_enrollment(db)
    }

@router_enrollment.post("/")
def create_enrollment(new_data: EnrollmentCreateReq, db: Session = Depends(getdb)):
    return{
        "message": "dang ky thanh cong",
        "data": create_enrollment_service(new_data, db)
    }