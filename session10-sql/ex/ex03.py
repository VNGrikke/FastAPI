"""
1.Phân tích bài toán
Vấn đề cốt lõi: Lỗi trùng lặp dữ liệu (Duplicate Entry) do người dùng thao tác nhầm sẽ sinh ra ngoại lệ IntegrityError từ MySQL, làm sập API (lỗi Server 500) nếu Backend xử lý thiếu phòng bị.

Mục tiêu xử lý: Thay đổi tư duy viết API từ "Cứ ghi dữ liệu, lỗi tính sau" sang tư duy "Hỏi trước, Ghi sau" (Kiểm tra bằng SELECT rồi mới INSERT).

Kỳ vọng: Định hình chuẩn dữ liệu đầu vào bằng Pydantic và trả về mã lỗi HTTP 400 thân thiện, rõ ràng thay vì để hệ thống tự văng lỗi kĩ thuật.

2.Giải pháp đề xuất
Chiến thuật "Truy vấn phủ đầu": Dùng SQLAlchemy ORM với cú pháp .filter().first() để quét Database xem mã kho (warehouse_code) đã tồn tại hay chưa ngay khi vừa nhận Request.

Bắt lỗi chủ động (Fail-Fast): Nếu phát hiện mã kho đã tồn tại, dùng lệnh raise HTTPException(status_code=400) để chặn đứng ngay lập tức toàn bộ luồng code bên dưới.

Ghi dữ liệu an toàn: Các lệnh thao tác Database thay đổi trạng thái (db.add(), db.commit()) được đặt ở cuối cùng. Chúng chỉ được kích hoạt khi chắc chắn 100% dữ liệu hoàn toàn hợp lệ và không bị trùng lặp.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
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

class InventoryModel(Base):
    __tablename__ = "inventories"
    id = Column(Integer, primary_key=True, index=True)
    warehouse_code = Column(String(50), unique=True, nullable=False)
    location = Column(String(100), nullable=False)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class InventoryCreate(BaseModel):
    warehouse_code: str
    location: str

@app.post("/inventories")
def add_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    print("Dữ liệu client gửi lên:", inventory)
    
    existing_inventory = db.query(InventoryModel).filter(
        InventoryModel.warehouse_code == inventory.warehouse_code
    ).first()
    
    if existing_inventory is not None:
        raise HTTPException(
            status_code=400,
            detail="Mã kho vận đã tồn tại trên hệ thống, không thể tạo trùng"
        )
        
    new_inventory = InventoryModel(
        warehouse_code=inventory.warehouse_code,
        location=inventory.location
    )
    
    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory) 
    
    return {
        "message": "Tạo mới kho vận thành công",
        "data": new_inventory
    }

@app.get("/inventories")
def get_all_inventories(db: Session = Depends(get_db)):
    inventories = db.query(InventoryModel).all()
    return {"message": "Lấy danh sách kho vận thành công", "data": inventories}