# validate du lieu tu client gui len va cau hinh respone tra ve

from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T')

class ResponseAPI(BaseModel, Generic[T]):
    status_code: int
    message: str
    data: Optional[T] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now) 
    path: str



class CreateProductReq(BaseModel):
    name: str = Field(..., max_length=50, description="Khong duoc de trong")
    price: float = Field(..., gt=0, description="Gia tri phai lon hon 0")

class UpdateProductReq(BaseModel):
    name: str = Field(max_length=50, description="Khong duoc de trong")
    price: float = Field(gt=0, description="Gia tri phai lon hon 0")