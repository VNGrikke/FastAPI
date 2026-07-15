"""
1. Phân tích Input / Output
Input: Nhận shipment_id (kiểu số nguyên) trực tiếp từ đường dẫn URL.

Output:

Thành công (200 OK): Trả về thông tin chi tiết của vận đơn.

Thất bại (404 Not Found): Bắt lỗi chủ động và trả về thông báo sạch sẽ (VD: "Không tìm thấy..."). Tuyệt đối không để rò rỉ mã lỗi thô hay làm sập server (lỗi 500).

2. Đánh giá hiệu năng & Lựa chọn
Giải pháp 1 (.all()): Kéo toàn bộ 100.000 dữ liệu lên RAM của Server rồi mới lọc. Cách này gây nghẽn mạng, ngốn RAM, làm chậm hệ thống và dễ gây sập (Out of Memory).

Giải pháp 2 (.first()): Truy vấn thẳng dưới Database với điều kiện lọc và LIMIT 1. Chỉ kéo đúng 1 dòng dữ liệu lên RAM, tốc độ phản hồi gần như tức thì.

Kết luận: Bắt buộc dùng Giải pháp 2 (.first()). Việc lọc dữ liệu phải để cho Database (MySQL) xử lý vì nó đã được tối ưu hóa cho việc này (thông qua Index). Bắt Python Server tải toàn bộ dữ liệu về rồi tự lọc là một sai lầm nghiêm trọng về thiết kế hệ thống.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy_utils import database_exists, create_database 
import urllib.parse

app = FastAPI()

raw_password = "a@1234"
encoded_password = urllib.parse.quote_plus(raw_password)

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{encoded_password}@localhost:3306/session10"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

if not database_exists(engine.url):
    create_database(engine.url)
    print("Đã tự động tạo database mới: session10")

Base = declarative_base()

class ShipmentModel(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    tracking_code = Column(String(50), unique=True, nullable=False)
    status = Column(String(50), default="Pending")
    destination = Column(String(100), nullable=False)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/shipments/{shipment_id}")
def get_shipment_detail(shipment_id: int, db: Session = Depends(get_db)):
    shipment = db.query(ShipmentModel).filter(ShipmentModel.id == shipment_id).first()
    
    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy mã vận đơn trên hệ thống"
        )
        
    return {
        "message": "Tra cứu thông tin vận đơn thành công",
        "data": shipment
    }