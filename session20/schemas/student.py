from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any
from enum import Enum
from schemas.classroom import ClassroomOut

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class StudentBase(BaseModel):
    student_code: str = Field(..., min_length=3, max_length=20)
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=16, le=60)
    gender: GenderEnum
    class_id: int = Field(..., ge=1)

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int
    classroom: Optional[ClassroomOut]

    class Config:
        orm_mode = True

# Định dạng Response chung đặt tại đây
class StandardResponse(BaseModel):
    statusCode: int
    message: str
    data: Any = None
    error: Optional[Any] = None
    timestamp: str
    path: str