from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Dữ liệu nội bộ trong bộ nhớ tạm
orders_db = [
    {
        "id": 1,
        "customer_name": "Nguyen Van A",
        "total_amount": 1500000.0,
        "profit_margin": 0.25,      # Nhạy cảm
        "supplier_id": "SUP_DELL_01"# Nhạy cảm
    },
    {
        "id": 2,
        "customer_name": "Tran Thi B",
        "total_amount": 350000.0,
        "profit_margin": 0.30,       # Nhạy cảm
        "supplier_id": "SUP_LOGI_02" # Nhạy cảm
    }
]

class OrderInternal(BaseModel):
    id: int
    customer_name: str
    total_amount: float
    profit_margin: float
    supplier_id: str

class OrderPublic(BaseModel):
    id: int
    customer_name: str
    total_amount: float

@app.get("/orders/{order_id}", response_model=OrderPublic)
def get_order_detail(order_id: int):
    for order in orders_db:
        if order["id"] == order_id:
            return order 
            
    raise HTTPException(status_code=404, detail="Order not found")



# STT	  Dữ liệu gửi lên	            Kết quả hiện tại (Mã HTTP + Body)	        Kết quả đúng mong muốn	                Lỗi phát hiện
# 1	      order_id = 999                HTTP: 200 OK                                HTTP: 404 Not Found                     Sai HTTP Status Code. Hệ thống không báo lỗi 404 khi không tìm thấy dữ liệu mà vẫn báo thành công (200).

#                                       Body:                                       Body:

#                                       {"message": "Order not found"}              {"detail": "Order not found"}


# 2       order_id = 1                  HTTP: 200 OK                                HTTP: 404 Not Found                     Rò rỉ dữ liệu nhạy cảm (Data Exposure). API trả về toàn bộ dữ liệu nội bộ bao gồm cả biên lợi nhuận và mã nhà cung cấp.

#                                       Body:                                       Body:

#                                       {"id": 1,                                   {"id": 1, 
#                                        "customer_name": "Nguyen Van A",           "customer_name": "Nguyen Van A", 
#                                        "total_amount": 1500000.0,                 "total_amount": 1500000.0}
#                                        "profit_margin": 0.25, 
#                                        "supplier_id": "SUP_DELL_01"}             
