from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy_utils import database_exists, create_database 
import urllib.parse
from pydantic import BaseModel

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

class ShipmentCreate(BaseModel):
    tracking_number: str




@app.post("/shipments", status_code=status.HTTP_201_CREATED)
def create_shipment(shipment: ShipmentCreate, db: Session = Depends(get_db)):
    existing_shipment = db.query(ShipmentModel).filter(
        ShipmentModel.tracking_number == shipment.tracking_number
    ).first()
    
    if existing_shipment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã vận đơn này đã được khởi tạo trước đó"
        )
        
    new_shipment = ShipmentModel(
        tracking_number=shipment.tracking_number
    )
    
    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment) 
    
    return {
        "message": "Đăng ký vận đơn thành công",
        "data": new_shipment
    }

@app.get("/shipments", status_code=status.HTTP_200_OK)
def get_all_shipments(db: Session = Depends(get_db)):
    shipments = db.query(ShipmentModel).all()
    
    return {
        "message": "Lấy danh sách vận đơn thành công",
        "data": shipments
    }