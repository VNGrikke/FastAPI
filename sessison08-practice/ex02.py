from enum import Enum
from fastapi import FastAPI, Request, status as http_status, Query
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime
import re

class AppException(Exception):
    """Class gốc cho mọi lỗi nghiệp vụ trong hệ thống."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

class AssetNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_404_NOT_FOUND, 
            message="Asset not found"
        )

class DuplicateSerialNumberError(AppException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_409_CONFLICT, 
            message="Serial number da ton tai trong he thong"
        )

class AssetNotReadyError(AppException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_400_BAD_REQUEST, 
            message="Thiet bi hien khong trong trang thai READY de cap phat"
        )

class InsufficientStockError(AppException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_400_BAD_REQUEST, 
            message="So luong ton kho kha dung khong du de cap phat"
        )

assets = [
    {"id": 1, "serial_number": "SN-MAC-01", "model": "MacBook Pro M3", "stock_available": 5, "status": "READY"},
    {"id": 2, "serial_number": "SN-DELL-02", "model": "Dell UltraSharp 27", "stock_available": 10, "status": "READY"},
    {"id": 3, "serial_number": "SN-THINK-03", "model": "ThinkPad X1 Carbon", "stock_available": 0, "status": "REPAIRING"}
]

allocations = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": "2026-07-01",
        "duration_months": 12
    }
]

class StandardResponse(BaseModel):
    statusCode: int
    message: str
    data: Any | None = None
    error: Any | None = None
    timestamp: str
    path: str

class AssetStatus(str, Enum):
    READY = "READY"
    ALLOCATED = "ALLOCATED"
    REPAIRING = "REPAIRING"
    SCRAPPED = "SCRAPPED"

class CreateAssetRequest(BaseModel):
    serial_number: str = Field(..., description="Serial Number, khong duoc de trong")
    model: str = Field(..., min_length=2, max_length=255, description="Ten model thiest bi tu 2 den 255 ky tu")
    stock_available: int = Field(..., ge=0, description="So luong ton kho phai >= 0")
    status: AssetStatus

class UpdateAssetRequest(BaseModel):
    model: str = Field(..., min_length=2, max_length=255)
    stock_available: int = Field(..., ge=0)
    status: AssetStatus

class CreateAllocationRequest(BaseModel):
    asset_id: int = Field(..., description="ID thiet bi can cap phat")
    employee_email: str = Field(
        ..., 
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", 
        description="Email nhan su phai dung dinh dang"
    )
    allocated_quantity: int = Field(..., gt=0, description="So luong cap phat phai lon hon 0")
    start_date: str = Field(..., description="Ngay bat dau cap phat (YYYY-MM-DD)")
    duration_months: int = Field(..., ge=1, le=12, description="Thoi gian cho muo tu 1 den 12 thang")

# Helper functions
def find_asset_by_id(asset_id: int): 
    for a in assets:
        if a["id"] == asset_id: return a
    return None

def check_duplicate_serial(serial: str):
    for a in assets:
        if a["serial_number"] == serial: return a
    return None

app = FastAPI()

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "message": exc.message,
            "data": None,
            "error": exc.__class__.__name__, 
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "statusCode": http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Du lieu dau vao khong hop le",
            "data": None,
            "error": exc.errors(),
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

@app.get("/assets", response_model=StandardResponse)
def get_assets(
    request: Request, 
    keyword: str | None = None, 
    status: AssetStatus | None = None, 
    min_stock: int | None = Query(None, ge=0)
):
    filter_result = assets

    if keyword is not None:
        keyword_lower = keyword.lower()
        filter_result = [
            a for a in filter_result 
            if keyword_lower in a["serial_number"].lower() or keyword_lower in a["model"].lower()
        ]

    if status is not None:
        filter_result = [a for a in filter_result if a["status"] == status.value]
    
    if min_stock is not None:
        filter_result = [a for a in filter_result if a["stock_available"] >= min_stock]

    return StandardResponse(
        statusCode=http_status.HTTP_200_OK, 
        message="Lay danh sach thiet bi thanh cong",
        data=filter_result,
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )

@app.get("/assets/{asset_id}", response_model=StandardResponse)
def detail_asset(request: Request, asset_id: int):
    asset = find_asset_by_id(asset_id)
    if asset is None:
        raise AssetNotFoundError()
        
    return StandardResponse(
        statusCode=http_status.HTTP_200_OK, 
        message="Lay chi tiet thiet bi thanh cong",
        data=asset,
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )

@app.post("/assets", response_model=StandardResponse, status_code=http_status.HTTP_201_CREATED)
def create_asset(req_body: CreateAssetRequest, request: Request):
    if check_duplicate_serial(req_body.serial_number):
        raise DuplicateSerialNumberError()
        
    new_id = max([a["id"] for a in assets], default=0) + 1
    new_asset = req_body.model_dump()
    new_asset["id"] = new_id
    
    assets.append(new_asset)
    
    return StandardResponse(
        statusCode=http_status.HTTP_201_CREATED,
        message="Khai bao thiet bi moi thanh cong",
        data=new_asset, 
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )

@app.put("/assets/{asset_id}", response_model=StandardResponse)
def update_asset(asset_id: int, req_body: UpdateAssetRequest, request: Request):
    asset = find_asset_by_id(asset_id)
    if asset is None:
        raise AssetNotFoundError()
    
    asset["model"] = req_body.model
    asset["stock_available"] = req_body.stock_available
    asset["status"] = req_body.status.value

    return StandardResponse(
        statusCode=http_status.HTTP_200_OK,
        message="Cap nhat thong tin thiet bi thanh cong",
        data=asset,
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )

@app.delete("/assets/{asset_id}", response_model=StandardResponse)
def del_asset(asset_id: int, request: Request):
    asset = find_asset_by_id(asset_id)
    if asset is None:
        raise AssetNotFoundError()
    
    assets.remove(asset)

    return StandardResponse(
        statusCode=http_status.HTTP_200_OK,
        message="Xoa thiet bi thanh cong",
        data=asset,
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )

@app.get("/allocations", response_model=StandardResponse)
def get_allocations(request: Request):
    return StandardResponse(
        statusCode=http_status.HTTP_200_OK, 
        message="Lay lich su cap phat thanh cong",
        data=allocations,
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )

@app.post("/allocations", response_model=StandardResponse, status_code=http_status.HTTP_201_CREATED)
def create_allocation(req_body: CreateAllocationRequest, request: Request):
    asset = find_asset_by_id(req_body.asset_id)
    
    # 1. Kiểm tra tồn tại
    if asset is None:
        raise AssetNotFoundError()
        
    if asset["status"] != AssetStatus.READY.value:
        raise AssetNotReadyError()
        
    if req_body.allocated_quantity > asset["stock_available"]:
        raise InsufficientStockError()

    asset["stock_available"] -= req_body.allocated_quantity

    new_id = max([al["id"] for al in allocations], default=0) + 1
    new_allocation = req_body.model_dump()
    new_allocation["id"] = new_id
    
    allocations.append(new_allocation)
    
    return StandardResponse(
        statusCode=http_status.HTTP_201_CREATED,
        message="Cap phat thiet bi thanh cong",
        data={
            "allocation": new_allocation,
            "asset_remaining_stock": asset["stock_available"]
        }, 
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )