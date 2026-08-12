from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List
from datetime import datetime, timezone
from enum import Enum

T = TypeVar("T")

class StatusEnum(str, Enum):
    AVAILABLE = "AVAILABLE"
    OUT_OF_STOCK = "OUT_OF_STOCK"

class MenuItemBase(BaseModel):
    dish_code: str = Field(..., min_length=1, description="Mã món ăn, không được để rỗng")
    dish_name: str = Field(..., min_length=1, description="Tên món ăn, không được để rỗng")
    calorie_count: int = Field(..., gt=0, description="Hàm lượng calo phải lớn hơn 0")
    price: float = Field(..., gt=0, description="Đơn giá phải lớn hơn 0")
    status: StatusEnum = Field(default=StatusEnum.AVAILABLE, description="Trạng thái món ăn")

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    dish_code: Optional[str] = Field(None, min_length=1)
    dish_name: Optional[str] = Field(None, min_length=1)
    calorie_count: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[StatusEnum] = None

class MenuItemResponse(MenuItemBase):
    id: int

    class Config:
        from_attributes = True

class StandardResponse(BaseModel, Generic[T]):
    statusCode: int
    message: str
    error: Optional[str] = None
    data: Optional[T] = None
    path: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))