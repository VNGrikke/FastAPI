from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session
from app.database.database import getdb
from app.models.students import Student
from app.models.classrooms import ClassRoom
from app.schemas.student import CreateStudent, UpdateStudent

router_student = APIRouter(
    prefix= "/students",
    tags=["student"]
)

@router_student.get("/")
def get_all_student(db: Session = Depends(getdb)):
    student = db.query(Student).all()
    return{
        "message": "Danh sach hoc sinh",
        "data": student
    }

@router_student.get("/{id}")
def get_student(id: int, db: Session = Depends(getdb)):
    student = db.query(Student).filter(Student.id == id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Không tìm thấy học sinh này")
        
    return{
        "message": "Chi tiet hoc sinh",
        "data": student
    }

@router_student.post("/")
def create_student(new_stu: CreateStudent,  db: Session = Depends(getdb)):
    classroom = db.query(ClassRoom).filter(ClassRoom.id == new_stu.class_id).first()
    
    if not classroom:
        raise HTTPException(status_code=404, detail="Không tìm thấy lớp học này")

    student_data = new_stu.model_dump()
    db_student = Student(**student_data) 

    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    return{
            "message": "Them moi hoc sinh thanh cong",
            "data": db_student
        }

@router_student.put("/{id}")
def update_student(id: int, new_stu: UpdateStudent,  db: Session = Depends(getdb)):
    student = db.query(Student).filter(Student.id == id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Hoc sinh khong ton tai")

    update_data = new_stu.model_dump(exclude_unset=True) 
    
    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    
    return{
            "message": "Cap nhat thong tin hoc sinh thanh cong",
            "data": student
        }

@router_student.delete("/{id}")
def delete_student(id: int, db: Session = Depends(getdb)):
    student = db.query(Student).filter(Student.id == id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Hoc sinh khong ton tai")
        
    db.delete(student)
    db.commit()
    
    return{
        "message": f"Da xoa thanh cong hoc sinh co ID: {id}"
    }