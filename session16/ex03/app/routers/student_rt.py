from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from session16.ex03.app.models.students_md import Student
from session16.ex03.app.database.database import get_db
from session16.ex03.app.schemas import StudentCoursesResponse


router_student = APIRouter (
    prefix="/students",
    tags= ["Student"]
)

@router_student.get("/{student_id}/courses", response_model=StudentCoursesResponse)
def get_student_courses(student_id: int, db: Session = Depends(get_db)):
    return {
        "id": student_id,
        "full_name": "Nguyễn Văn An",
        "courses": [
            {
                "id": 2,
                "name": "FastAPI Basic"
            }
        ]
    }