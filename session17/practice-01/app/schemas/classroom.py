from pydantic import BaseModel, Field
from typing import Optional

class ClassRoomBase(BaseModel):
    class_name: str = Field(..., max_length=50, min_length=1, description="Tên của lớp học")

class CreateClassRoom(ClassRoomBase):
    pass  

class UpdateClassRoom(BaseModel):
    class_name: Optional[str] = Field(None, max_length=50, min_length=1)

class ClassRoomResponse(ClassRoomBase):
    id: int

    model_config = {"from_attributes": True}