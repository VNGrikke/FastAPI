from pydantic import BaseModel, EmailStr
from typing import List
from .student import StudentStatus

class StudentCreateReq(BaseModel):
    student_code: str
    full_name: str
    email: EmailStr

# Schema hiển thị cơ bản
class StudentResponse(BaseModel):
    id: int
    student_code: str
    full_name: str
    email: str
    status: StudentStatus

    class Config:
        from_attributes = True

class StudentWithWorkshopsResponse(StudentResponse):
    pass