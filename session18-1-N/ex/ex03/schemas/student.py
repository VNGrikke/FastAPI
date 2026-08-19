from pydantic import BaseModel, Field
from enum import Enum
from typing import List
from ..schemas.enrollment import EnrollmentDetail

class EnumStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class StudentBase(BaseModel):
    full_name : str = Field(..., max_length=100)
    status : EnumStatus

class StudentCreateReq(StudentBase):
    pass

class StudentUpdateReq(StudentBase):
    pass

class StudentWithCoursesResponse(BaseModel):
    id: int
    full_name: str
    status: str
    courses: List[EnrollmentDetail] = Field(default=[], validation_alias="enrollments")
    class Config:
        from_attributes = True 

class BaseResponseStudentDetail(BaseModel):
    message: str
    data: StudentWithCoursesResponse