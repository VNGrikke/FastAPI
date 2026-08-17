from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from session16.ex03.app.database.database import get_db
from session16.ex03.app.schemas import EnrollmentCreate, EnrollmentResponse

router_enrollment = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)

@router_enrollment.post("", response_model=EnrollmentResponse, status_code=201)
def enroll_student(enrollment_data: EnrollmentCreate, db: Session = Depends(get_db)):
    return {
        "id": 5,
        "student_id": enrollment_data.student_id,
        "course_id": enrollment_data.course_id,
        "enrolled_at": "2026-07-13T10:30:00"
    }