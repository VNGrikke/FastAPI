from pydantic import BaseModel

class ClassroomOut(BaseModel):
    id: int
    class_code: str
    class_name: str
    status: str

    class Config:
        orm_mode = True