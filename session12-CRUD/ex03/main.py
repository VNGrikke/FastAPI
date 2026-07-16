from fastapi import Depends, FastAPI
from database import SessionLocal, engine
import models
from sqlalchemy.orm import Session
from service import update_shipment_service
from pydantic import BaseModel

models.Base.metadata.create_all(engine)

class ShipmentUpdate(BaseModel):
    receiver_name: str
    delivery_address: str



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "API quản lý đơn hàng đang chạy"
    }

@app.put("/shipments/{shipment_id}")
def update_shipment(
    shipment_id: int, 
    shipment_update: ShipmentUpdate, 
    db: Session = Depends(get_db)
):
    return update_shipment_service(db, shipment_id, shipment_update)