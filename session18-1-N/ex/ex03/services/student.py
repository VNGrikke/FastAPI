from sqlalchemy.orm import selectinload, load_only
from fastapi import HTTPException, status
from ..models.student import Student
from ..models.course import Course
from ..models.enrollment import Enrollment

def get_all_student(db):
    return db.query(Student).all()

def create_student_service(data, db):
    data_student = data.model_dump()

    db_student = Student(**data_student)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student

def get_student_with_courses(student_id: int, db):
    student = db.query(Student).options(
        selectinload(Student.enrollments)
        .selectinload(Enrollment.course)
        .load_only(Course.id, Course.name) 
    ).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    return student