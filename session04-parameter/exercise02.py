# Có.
# Path Parameter là status (được khai báo trong đường dẫn URL dưới dạng {status}).
# Biến status sẽ nhận giá trị là chuỗi "pending".
# Vì hàm xử lý get_orders_by_status không thực hiện bất kỳ thao tác lọc (filter) nào với tham số status được truyền vào, mà chỉ đơn thuần trả về toàn bộ danh sách orders gốc.
# Đó là dòng: return orders.


from fastapi import FastAPI
app = FastAPI()
orders = [
    {"id": 1, "customer_name": "Nguyễn Văn An", "total": 250000, "status": "pending"},
    {"id": 2, "customer_name": "Trần Thị Bình", "total": 500000, "status": "paid"},
    {"id": 3, "customer_name": "Lê Văn Cường", "total": 150000, "status": "cancelled"},
    {"id": 4, "customer_name": "Phạm Thị Dung", "total": 320000, "status": "pending"}
]
@app.get("/orders/status/{status}")
def get_orders_by_status(status: str):
    valid_statuses = ["pending", "paid", "cancelled"]
    
    if status not in valid_statuses:
        return {"message": "Trạng thái đơn hàng không hợp lệ"}
    
    filtered_orders = [order for order in orders if order["status"] == status]
    
    return filtered_orders