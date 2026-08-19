from pydantic import BaseModel, Field
from enum import Enum

class EnumStatus(str, Enum):
    ACTIVE = "OPEN"
    INACTIVE = "CLOSE"


class CourseCreateReq(BaseModel):
    name: str = Field(..., max_length=100)
    max_students: int = Field(..., gt=0) 
    status: EnumStatus