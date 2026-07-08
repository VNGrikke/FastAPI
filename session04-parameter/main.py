from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

students = [
    {"id": 1, "name": "Vuong", "address": "hd"},
    {"id": 2, "name": "Vuong2", "address": "hd"},
    {"id": 3, "name": "Vuong3", "address": "hd"},
    {"id": 4, "name": "Vuong4", "address": "hd"},
]

class Student(BaseModel):
    id: int
    name: str
    address: str

class UpdateStudent(BaseModel):
    name: str = Field(min_length=5, max_length=10)
    address: Optional[str] = None

@app.get("/students/{id}")
def get_student(id: int):
    return f"Thong tin chi tiet cua sinh vien {id}"

@app.get("/students")
def get_students(keyword: str = None, limit: int = 10, skip: int = 1):
    return "API lay danh sach"

@app.post("/students")
def create_student(student: Student):
    students.append(student.model_dump()) 
    return students

@app.put("/student/{id_student}")
def update_student(update: UpdateStudent, id_student: int):
    for student in students:
        if student["id"] == id_student:
            student["name"] = update.name
            
            if update.address is not None:
                student["address"] = update.address
                
            return student 
    
    # Trả về mã lỗi 404 chuẩn của FastAPI nếu không tìm thấy
    raise HTTPException(status_code=404, detail=f"Khong tim thay sinh vien id: {id_student}")