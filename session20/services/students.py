from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.students import Student
from models.classrooms import Classroom
from schemas.student import StudentCreate, StudentUpdate

class StudentService:
    @staticmethod
    def _check_class_availability(db: Session, class_id: int):
        classroom = db.query(Classroom).filter(Classroom.id == class_id).first()
        if not classroom:
            raise HTTPException(status_code=400, detail="Lớp học không tồn tại.")
        if classroom.status != "active":
            raise HTTPException(status_code=400, detail="Lớp học không ở trạng thái active.")
        if len(classroom.students) >= classroom.max_students:
            raise HTTPException(status_code=400, detail="Lớp học đã đủ số lượng sinh viên.")
        return classroom

    @staticmethod
    def get_students(db: Session, name: str = None, code: str = None, email: str = None, class_id: int = None):
        query = db.query(Student)
        if name:
            query = query.filter(Student.full_name.ilike(f"%{name}%"))
        if code:
            query = query.filter(Student.student_code.ilike(f"%{code}%"))
        if email:
            query = query.filter(Student.email.ilike(f"%{email}%"))
        if class_id:
            query = query.filter(Student.class_id == class_id)
        return query.all()

    @staticmethod
    def get_student_by_id(db: Session, student_id: int):
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên.")
        return student

    @staticmethod
    def create_student(db: Session, student: StudentCreate):
        StudentService._check_class_availability(db, student.class_id)

        if db.query(Student).filter(Student.student_code == student.student_code).first():
            raise HTTPException(status_code=400, detail="Mã sinh viên đã tồn tại.")
        if db.query(Student).filter(Student.email == student.email).first():
            raise HTTPException(status_code=400, detail="Email đã tồn tại.")

        db_student = Student(**student.dict())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student

    @staticmethod
    def update_student(db: Session, student_id: int, student_data: StudentUpdate):
        db_student = StudentService.get_student_by_id(db, student_id)

        if db_student.class_id != student_data.class_id:
            StudentService._check_class_availability(db, student_data.class_id)

        if db.query(Student).filter(Student.student_code == student_data.student_code, Student.id != student_id).first():
            raise HTTPException(status_code=400, detail="Mã sinh viên đã tồn tại ở hồ sơ khác.")
        if db.query(Student).filter(Student.email == student_data.email, Student.id != student_id).first():
            raise HTTPException(status_code=400, detail="Email đã tồn tại ở hồ sơ khác.")

        for key, value in student_data.dict().items():
            setattr(db_student, key, value)

        db.commit()
        db.refresh(db_student)
        return db_student

    @staticmethod
    def delete_student(db: Session, student_id: int):
        db_student = StudentService.get_student_by_id(db, student_id)
        db.delete(db_student)
        db.commit()