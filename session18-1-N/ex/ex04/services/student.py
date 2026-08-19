from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException
from models.student import Student
from models.workshop import Workshop, Registration

def create_student_service(data, db: Session):
    db_student = Student(**data.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_all_students_service(db: Session):
    return db.query(Student).all()

def get_student_with_workshops(student_id: int, db: Session):
    student = db.query(Student).options(
        selectinload(Student.registrations)
        .selectinload(Registration.workshop)
    ).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")
    return student