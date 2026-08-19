from pydantic import BaseModel
from typing import List, Optional

# --- PACKAGE SCHEMAS ---
class PackageBase(BaseModel):
    package_code: str
    weight: float

class PackageResponse(PackageBase):
    id: int
    warehouse_id: int

    class Config:
        from_attributes = True

class PackageUpdate(BaseModel):
    package_code: Optional[str] = None
    weight: Optional[float] = None
    warehouse_id: Optional[int] = None

# --- WAREHOUSE SCHEMAS ---
class WarehouseCreate(BaseModel):
    warehouse_name: str
    location: str

class WarehouseDetailResponse(BaseModel):
    id: int
    warehouse_name: str
    location: str
    packages: List[PackageResponse] = [] 
    class Config:
        from_attributes = True

# --- WAYBILL SCHEMAS ---
class WaybillResponse(BaseModel):
    id: int
    tracking_number: str
    shipping_status: str
    package_id: int

    class Config:
        from_attributes = True