from typing import List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field
import urllib.parse
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship,
    Session
)
from sqlalchemy_utils import create_database, database_exists

encode_password = urllib.parse.quote_plus("a@1234")

DATABASE_URL = f"mysql+pymysql://root:{encode_password}@localhost:3306/ss18"
engine = create_engine(DATABASE_URL)

if not database_exists(engine.url):
    create_database(engine.url)
    
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()

class Classroom(Base):
    __tablename__ = "classrooms"
    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)
    capacity = Column(Integer, nullable=False)
    students = relationship(
        "Student",
        back_populates="classroom"
    )
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    student_code = Column(String(20), nullable=False)
    full_name = Column(String(100), nullable=False)
    classroom_id = Column(
        Integer,
        ForeignKey("classrooms.id"),
        nullable=False
    )
    classroom = relationship(
        "Classroom",
        back_populates="students"
    )
Base.metadata.create_all(bind=engine)
class ClassroomCreate(BaseModel):
    class_name: str
    status: str
    capacity: int
class StudentCreate(BaseModel):
    student_code: str
    full_name: str
    classroom_id: int
class TransferClassRequest(BaseModel):
    new_classroom_id: int

class StudentResponse(BaseModel):
    id: int
    student_code: str
    full_name: str
    classroom_id: int
    model_config = ConfigDict(from_attributes=True)
class ClassroomDetailResponse(BaseModel):
    id: int
    class_name: str
    status: str
    capacity: int
    students: List[StudentResponse] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)
app = FastAPI(
    title="Classroom Student API"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/classrooms")
def create_classroom(
    data: ClassroomCreate,
    db: Session = Depends(get_db)
):
    classroom = Classroom(
        class_name=data.class_name,
        status=data.status,
        capacity=data.capacity
    )
    db.add(classroom)
    db.commit()
    db.refresh(classroom)
    return classroom

@app.post(
    "/students",
    response_model=StudentResponse
)
def create_student(
    data: StudentCreate,
    db: Session = Depends(get_db)
):
    classroom = (
        db.query(Classroom)
        .filter(Classroom.id == data.classroom_id)
        .first()
    )
    if classroom is None:
        raise HTTPException(
            status_code=404,
            detail="Lớp học không tồn tại"
        )
    if classroom.status != "OPEN":
        raise HTTPException(
            status_code=400,
            detail="Lớp học đã đóng"
        )
    current_count = (
        db.query(Student)
        .filter(Student.classroom_id == data.classroom_id)
        .count()
    )
    if current_count >= classroom.capacity:
        raise HTTPException(
            status_code=400,
            detail="Lớp học đã đủ sinh viên"
        )
    student = Student(
        student_code=data.student_code,
        full_name=data.full_name,
        classroom_id=data.classroom_id
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@app.get(
    "/classrooms/{classroom_id}",
    response_model=ClassroomDetailResponse
)
def get_classroom_detail(
    classroom_id: int,
    db: Session = Depends(get_db)
):
    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()
    
    if classroom is None:
        raise HTTPException(
            status_code=404,
            detail="Lớp học không tồn tại"
        )
    
    return classroom

@app.put(
    "/students/{student_id}/transfer",
    response_model=StudentResponse
)
def transfer_student(
    student_id: int,
    data: TransferClassRequest,
    db: Session = Depends(get_db)
):
    # 1. Tìm sinh viên theo student_id
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )

    # 2. Tìm lớp học đích theo new_classroom_id
    target_classroom = db.query(Classroom).filter(Classroom.id == data.new_classroom_id).first()
    if target_classroom is None:
        raise HTTPException(
            status_code=404,
            detail="Lớp học đích không tồn tại"
        )

    # 3. Kiểm tra trạng thái lớp đích
    if target_classroom.status == "CLOSED":
        raise HTTPException(
            status_code=400,
            detail="Lớp học đích đã đóng"
        )

    # 4. Đếm số sinh viên hiện tại của lớp đích
    current_count = (
        db.query(Student)
        .filter(Student.classroom_id == data.new_classroom_id)
        .count()
    )
    
    # Nếu số sinh viên hiện tại lớn hơn hoặc bằng sức chứa
    if current_count >= target_classroom.capacity:
        raise HTTPException(
            status_code=400,
            detail="Lớp học đích đã đủ sinh viên"
        )

    # 5. Cập nhật classroom_id của sinh viên
    student.classroom_id = data.new_classroom_id
    
    # 6. Lưu thay đổi
    db.commit()
    db.refresh(student)
    
    # 7. Trả về thông tin sinh viên
    return student


@app.get("/students/{id}")
def get_detail_student(id: int, db: Session= Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()

    return student.classroom