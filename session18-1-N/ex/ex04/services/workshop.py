from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException
from models.workshop import Workshop, Registration, WorkshopStatus, RegistrationStatus
from models.student import Student, StudentStatus

def get_workshop_with_students(workshop_id: int, db: Session):
    workshop = db.query(Workshop).options(
        selectinload(Workshop.registrations)
        .selectinload(Registration.student)
    ).filter(Workshop.id == workshop_id).first()
    
    if not workshop:
        raise HTTPException(status_code=404, detail="Không tìm thấy workshop")
    return workshop

def register_student_to_workshop(student_id: int, workshop_id: int, db: Session):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student or student.status != StudentStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Sinh viên không tồn tại hoặc bị khóa.")

    workshop = db.query(Workshop).filter(Workshop.id == workshop_id).first()
    if not workshop or workshop.status != WorkshopStatus.UPCOMING:
        raise HTTPException(status_code=400, detail="Workshop không tồn tại hoặc đã đóng.")

    existing = db.query(Registration).filter(
        Registration.student_id == student_id,
        Registration.workshop_id == workshop_id,
        Registration.status == RegistrationStatus.REGISTERED
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Đã đăng ký workshop này rồi.")

    count = db.query(Registration).filter(
        Registration.workshop_id == workshop_id,
        Registration.status == RegistrationStatus.REGISTERED
    ).count()
    
    if count >= workshop.max_participants:
        raise HTTPException(status_code=400, detail="Workshop đã đầy.")

    new_reg = Registration(student_id=student_id, workshop_id=workshop_id)
    db.add(new_reg)
    db.commit()
    db.refresh(new_reg)
    return new_reg