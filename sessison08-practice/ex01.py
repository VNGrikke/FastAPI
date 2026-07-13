from enum import Enum
from fastapi import FastAPI, Request, status as http_status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime

class AppException(Exception):
    """Class gốc cho mọi lỗi nghiệp vụ trong hệ thống."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

class CarrierNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_404_NOT_FOUND, 
            message="Doi tac van chuyen khong ton tai"
        )

class DuplicateCarrierCodeError(AppException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_409_CONFLICT, 
            message="Code da ton tai"
        )

class ExceedWeightCapacityError(AppException):
    def __init__(self):
        super().__init__(
            status_code=http_status.HTTP_400_BAD_REQUEST, 
            message="Tong khoi luong vuot qua tai trong toi da cua doi tac van chuyen"
        )
# ==========================================
# DỮ LIỆU & MODELS
# ==========================================
carriers = [
    {"id": 1, "code": "GHN", "name": "Giao Hang Nhanh", "max_weight_capacity": 5000, "status": "ACTIVE"},
    {"id": 2, "code": "GHTK", "name": "Giao Hang Tiet Kiem", "max_weight_capacity": 3000, "status": "ACTIVE"},
    {"id": 3, "code": "VTP", "name": "Viettel Post", "max_weight_capacity": 10000, "status": "SUSPENDED"}
]


shipments = [
    {
        "id": 1,
        "carrier_id": 1,
        "order_reference": "ORD-2026-001",
        "total_weight": 4200,
        "dispatch_date": "2026-07-01",
        "shift": "MORNING"
    }
]


class StandardResponse(BaseModel):
    statusCode: int
    message: str
    data: Any | None = None
    error: Any | None = None
    timestamp: str
    path: str

class ShiftType(str, Enum):
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"
    EVENING = "EVENING"

class CreateShipmentRequest(BaseModel):
    carrier_id: int = Field(..., description="ID của đối tác vận chuyển")
    order_reference: str = Field(..., description="Mã tham chiếu đơn hàng, không được để trống")
    total_weight: int = Field(..., gt=0, description="Tổng khối lượng (gram), phải lớn hơn 0")
    dispatch_date: str = Field(..., description="Ngày giao hàng (YYYY-MM-DD)")
    shift: ShiftType

class CarrieStatus(str, Enum): 
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"

class CreateCarriersRequest(BaseModel):
    code: str = Field(..., description="khong duoc de trong")
    name: str = Field(..., min_length=3, description="khong duoc de trong")
    max_weight_capacity: int = Field(..., gt=0, description="Phai lon hon 0")
    status: CarrieStatus

def find_carrier_by_id(carrier_id: int): 
    for c in carriers:
        if c["id"] == carrier_id: return c
    return None

def check_duplicate_code(carrier_code: str):
    for c in carriers:
        if c["code"] == carrier_code: return c
    return None

app = FastAPI()

# ==========================================
# 2. GLOBAL EXCEPTION HANDLERS
# ==========================================

# Handler chuyên biệt cho các lỗi nghiệp vụ do bạn tự định nghĩa
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "message": exc.message,
            "data": None,
            "error": exc.__class__.__name__, # Trả về tên của Exception (VD: CarrierNotFoundError)
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

# Handler bắt lỗi Pydantic (Thiếu data, sai kiểu dữ liệu)
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



# ==========================================
# 3. API ROUTES (Đã được làm sạch)
# ==========================================

@app.get("/carriers", response_model=StandardResponse)
def get_carriers(request: Request, keywords: str | None = None, status: CarrieStatus | None = None, min_weight: int | None = None):
    filter_result = carriers

    if keywords is not None:
        keywords = keywords.lower()
        filter_result = [c for c in filter_result if keywords in c["code"].lower() or keywords in c["name"].lower()]

    if status is not None:
        filter_result = [c for c in filter_result if c["status"] == status.value]
    
    if min_weight is not None:
        filter_result = [c for c in filter_result if c["max_weight_capacity"] >= min_weight]

    return StandardResponse(
        statusCode=http_status.HTTP_200_OK, 
        message="Lay danh sach doi tac van chuyen thanh cong",
        data=filter_result,
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )


@app.get("/carriers/{carrier_id}", response_model=StandardResponse)
def detail_carrier(request: Request, carrier_id: int):
    carrier = find_carrier_by_id(carrier_id)
    
    if carrier is None:
        # Ném lỗi ra ngoài. Global handler sẽ chụp lại và trả về 404 StandardResponse!
        raise CarrierNotFoundError()
        
    return StandardResponse(
        statusCode=http_status.HTTP_200_OK, 
        message="Lay chi tiet doi tac van chuyen thanh cong",
        data=carrier,
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )


@app.post("/carriers", response_model=StandardResponse, status_code=http_status.HTTP_201_CREATED)
def create_carrier(create_carrier_req: CreateCarriersRequest, request: Request):
    if check_duplicate_code(create_carrier_req.code):
        # Ném lỗi ra ngoài. Global handler sẽ chụp lại và trả về 409 StandardResponse!
        raise DuplicateCarrierCodeError()
        
    new_carrier_id = max([c["id"] for c in carriers], default=0) + 1
    new_carrier = create_carrier_req.model_dump()
    new_carrier["id"] = new_carrier_id
    
    carriers.append(new_carrier)
    
    return StandardResponse(
        statusCode=http_status.HTTP_201_CREATED,
        message="Them moi thanh cong",
        data=new_carrier, 
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )


@app.delete("/carriers/{carrier_id}", response_model=StandardResponse)
def del_carrier(carrier_id: int, request: Request):
    carrier = find_carrier_by_id(carrier_id)
    if carrier is None:
        raise CarrierNotFoundError()
    
    carriers.remove(carrier)

    return StandardResponse(
        statusCode=http_status.HTTP_200_OK,
        message="Xoa thanh cong",
        data=carrier,
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )

@app.get("/shipments", response_model=StandardResponse)
def get_shipments(request: Request):
    return StandardResponse(
        statusCode=http_status.HTTP_200_OK, 
        message="Lay danh sach chuyen giao hang thanh cong",
        data=shipments,
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )

@app.post("/shipments", response_model=StandardResponse, status_code=http_status.HTTP_201_CREATED)
def create_shipment(create_shipment_req: CreateShipmentRequest, request: Request):
    carrier = find_carrier_by_id(create_shipment_req.carrier_id)
    if carrier is None:
        raise CarrierNotFoundError()
        
    new_shipment_id = max([s["id"] for s in shipments], default=0) + 1
    
    new_shipment = create_shipment_req.model_dump()
    new_shipment["id"] = new_shipment_id
    
    shipments.append(new_shipment)
    
    return StandardResponse(
        statusCode=http_status.HTTP_201_CREATED,
        message="Khoi tao chuyen giao hang moi thanh cong",
        data=new_shipment, 
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )