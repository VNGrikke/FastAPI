from pydantic import BaseModel
from datetime import datetime
from typing import List
from .workshop import WorkshopStatus

class StudentShortDetail(BaseModel):
    id: int
    full_name: str
    student_code: str

    class Config:
        from_attributes = True

class RegistrationDetail(BaseModel):
    registered_at: datetime
    student: StudentShortDetail

    class Config:
        from_attributes = True

class WorkshopResponse(BaseModel):
    id: int
    title: str
    max_participants: int
    status: WorkshopStatus

    class Config:
        from_attributes = True

class WorkshopWithStudentsResponse(WorkshopResponse):
    registrations: List[RegistrationDetail] = []