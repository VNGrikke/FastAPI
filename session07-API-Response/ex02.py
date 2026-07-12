from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

orders_db = [
    {"id": 1, "customer_name": "Nguyen Van A", "status": "PENDING"},
    {"id": 2, "customer_name": "Tran Thi B", "status": "SHIPPING"}
]

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    SHIPPING = "SHIPPING"
    DELIVERED = "DELIVERED"

class StatusUpdate(BaseModel):
    status: OrderStatus 

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, data: StatusUpdate):
    order = next((o for o in orders_db if o["id"] == order_id), None)
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    order["status"] = data.status.value 

    return {"statusCode": 200, "message": "Cập nhật thành công", "data": order}