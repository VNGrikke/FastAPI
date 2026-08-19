from ..models.enrollment import Enrollment
from ..models.student import Student
from ..models.course import Course
from fastapi import HTTPException, status

def get_all_enrollment(db):
    return db.query(Enrollment).all()

def create_enrollment_service(data, db):
    student = db.query(Student).filter(Student.id == data.student_id).first()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sinh vien khong ton tai"
        )
    if student.status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sinh vien khong trong trang thai hoat dong"
        )

    course = db.query(Course).filter(Course.id == data.course_id).first()
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khoa hoc khong ton tai"
        )
    if course.status != "OPEN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Khoa hoc chua duoc mo"
        )

    duplicate_enrollment = db.query(Enrollment).filter(
        Enrollment.course_id == data.course_id, 
        Enrollment.student_id == data.student_id
    ).first()
    
    if duplicate_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sinh vien da dang ki khoa hoc nay"
        )

    student_count = db.query(Enrollment).filter(Enrollment.course_id == data.course_id).count()
    if student_count >= course.max_students:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="So luong sinh vien da dat toi da"
        )

    data_enrollment = data.model_dump()
    db_enrollment = Enrollment(**data_enrollment)
    
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)

    return db_enrollment