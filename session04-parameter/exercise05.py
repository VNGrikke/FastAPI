from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

app = FastAPI()

registered_students = []

class StudentRegister(BaseModel):
    full_name: str = Field(..., min_length=3, strip_whitespace=True)
    email: EmailStr 
    age: int = Field(..., ge=15, le=60)
    phone: str = Field(..., min_length=10, max_length=11, pattern=r"^\d+$")
    course: str = Field(...)
    note: Optional[str] = Field(default=None, max_length=200)

@app.post("/students/register")
async def register_student(student: StudentRegister):
    new_student = student.model_dump()
    
    registered_students.append(new_student)
    
    return {
        "message": "Đăng ký học viên thành công",
        "data": new_student
    }

