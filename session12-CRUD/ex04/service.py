import models
from fastapi import HTTPException
from sqlalchemy.orm import Session

def delete_student_service(db: Session, student_id: int):
    student = db.query(models.StudentModel).filter(models.StudentModel.id == student_id).first()
    
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Học viên không tồn tại trong hệ thống"
        )
    
    deleted_data = {
        "id": student.id,
        "full_name": student.full_name,
        "email": student.email
    }
    
    db.delete(student)
    
    db.commit()
    
    return {
        "message": "Xóa học viên thành công",
        "data": deleted_data
    }