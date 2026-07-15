from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import urllib.parse

app = FastAPI()

raw_password = "a@1234"
encoded_password = urllib.parse.quote_plus(raw_password)
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{encoded_password}@localhost:3306/parking_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

if not database_exists(engine.url):
    create_database(engine.url)
    print("Đã tự động tạo database mới: parking_db")

Base = declarative_base()

class ParkingSlotModel(Base):
    __tablename__ = "parking_slots"
    
    id = Column(Integer, primary_key=True, index=True)
    slot_code = Column(String(50), unique=True, nullable=False) # Không trùng lặp
    zone_name = Column(String(255), nullable=False)
    max_weight = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ParkingSlotCreate(BaseModel):
    slot_code: str
    zone_name: str = Field(..., min_length=3, description="Tên khu vực tối thiểu 3 ký tự")
    max_weight: int = Field(..., gt=0, description="Tải trọng phải lớn hơn 0")
    is_available: bool = True

def get_current_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def format_response(request: Request, status_code: int, message: str, error: str | None = None, data: any = None):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": request.url.path,
        "timestamp": get_current_timestamp()
    }

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    error_type = "Not Found" if exc.status_code == 404 else "Bad Request"
    response_body = format_response(request, exc.status_code, exc.detail, error_type, None)
    return JSONResponse(status_code=exc.status_code, content=response_body)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    response_body = format_response(request, 400, "Dữ liệu đầu vào không hợp lệ", "Validation Error", None)
    return JSONResponse(status_code=400, content=response_body)

@app.post("/parking-slots", status_code=201)
def add_parking_slot(slot: ParkingSlotCreate, request: Request, db: Session = Depends(get_db)):
    new_slot = ParkingSlotModel(
        slot_code=slot.slot_code,
        zone_name=slot.zone_name,
        max_weight=slot.max_weight,
        is_available=slot.is_available
    )
    
    try:
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
        
        return format_response(request, 201, "Thêm vị trí đỗ xe thành công", None, new_slot)
        
    except IntegrityError:
        db.rollback() 
        raise HTTPException(status_code=400, detail="Mã vị trí đỗ bị trùng lặp trên hệ thống")
        
    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail="Lỗi hệ thống cơ sở dữ liệu")

@app.get("/parking-slots")
def get_all_parking_slots(request: Request, db: Session = Depends(get_db)):
    slots = db.query(ParkingSlotModel).all()
    return format_response(request, 200, "Lấy danh sách vị trí đỗ xe thành công", None, slots)

@app.get("/parking-slots/{slot_id}")
def get_parking_slot_detail(slot_id: int, request: Request, db: Session = Depends(get_db)):
    slot = db.query(ParkingSlotModel).filter(ParkingSlotModel.id == slot_id).first()
    
    if slot is None:
        raise HTTPException(status_code=404, detail="Parking slot not found")
        
    return format_response(request, 200, "Lấy chi tiết vị trí đỗ xe thành công", None, slot)