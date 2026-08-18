from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class StudentBase(BaseModel):
    name: str = Field(..., max_length=50, min_length=1, description="Tên học sinh")
    email: EmailStr = Field(..., description="Địa chỉ email của học sinh") 
    class_id: int = Field(..., description="ID của lớp học mà học sinh thuộc về")

class CreateStudent(StudentBase):
    pass  

class UpdateStudent(BaseModel):
    name: Optional[str] = Field(None, max_length=50, min_length=1)
    email: Optional[EmailStr] = Field(None)
    class_id: Optional[int] = Field(None)

class StudentResponse(StudentBase):
    id: int

    model_config = {"from_attributes": True}