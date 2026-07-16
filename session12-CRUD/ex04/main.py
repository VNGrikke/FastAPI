from fastapi import Depends, FastAPI
from database import SessionLocal, engine
import models
from sqlalchemy.orm import Session
from service import delete_student_service

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "API quản lý học viên đang chạy"
    }

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return delete_student_service(db, student_id)