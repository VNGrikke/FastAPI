from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import getdb
from app.models.classrooms import ClassRoom

from app.schemas.classroom import CreateClassRoom, UpdateClassRoom

router_classroom = APIRouter(
    prefix= "/classrooms",
    tags=["Classroom"]
)

@router_classroom.get("/")
def get_all_classroom(db: Session = Depends(getdb)):
    classrooms = db.query(ClassRoom).all()
    return{
        "message": "Danh sach lop hoc",
        "data": classrooms
    }

@router_classroom.get("/{id}")
def get_classroom(id: int, db: Session = Depends(getdb)):
    classroom = db.query(ClassRoom).filter(ClassRoom.id == id).first()
    
    if not classroom:
        raise HTTPException(status_code=404, detail="Không tìm thấy lớp học này")
        
    return{
        "message": "Chi tiet lop hoc",
        "data": classroom
    }

@router_classroom.post("/")
def create_classroom(new_class: CreateClassRoom, db: Session = Depends(getdb)):
    class_data = new_class.model_dump()
    db_class = ClassRoom(**class_data) 
    
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    
    return{
        "message": "Them moi lop hoc thanh cong",
        "data": db_class
    }

@router_classroom.put("/{id}")
def update_classroom(id: int, update_class: UpdateClassRoom, db: Session = Depends(getdb)):
    classroom = db.query(ClassRoom).filter(ClassRoom.id == id).first()
    
    if not classroom:
        raise HTTPException(status_code=404, detail="Không tìm thấy lớp học này")
        
    update_data = update_class.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(classroom, key, value)
        
    db.commit()
    db.refresh(classroom)
    
    return{
        "message": "Cap nhat thong tin lop hoc thanh cong",
        "data": classroom
    }

@router_classroom.delete("/{id}")
def delete_classroom(id: int, db: Session = Depends(getdb)):
    classroom = db.query(ClassRoom).filter(ClassRoom.id == id).first()
    
    if not classroom:
        raise HTTPException(status_code=404, detail="Không tìm thấy lớp học này")
        
    db.delete(classroom)
    db.commit()
    
    return{
        "message": f"Da xoa thanh cong lop hoc co ID: {id}"
    }