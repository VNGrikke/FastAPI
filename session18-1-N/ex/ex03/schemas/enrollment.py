from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class EnrollmentCreateReq(BaseModel):
    student_id : int = Field(..., gt=0)
    course_id : int = Field(..., gt=0)


class CourseShortDetail(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class EnrollmentDetail(BaseModel):
    course: CourseShortDetail 
    class Config:
        from_attributes = True


