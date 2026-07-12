# 1. Input / Output (I/O)
# Input: Tham số order_id (int) truyền qua URL.
# Output:
# Thành công: Mã 200 OK + Dữ liệu thanh toán.
# Bẫy 1 (Không tìm thấy): Mã 404 Not Found.
# Bẫy 2 (Lỗi Crash hệ thống): Mã 500 Internal Error (Tuyệt đối không lộ Stack Trace).
# 2. Đề xuất 2 giải pháp lưu trữ
# Giải pháp 1: Dùng Mảng (List) - Đậm chất "người mới"
# Cấu trúc: [{"id": 1, ...}, {"id": 2, ...}]
# Cách tra cứu: Phải dùng vòng lặp for chạy từ đầu đến cuối.
# Đánh giá: Rất chậm (O(n)). Đơn hàng thứ 10.000 phải lặp 10.000 lần.
# Giải pháp 2: Dùng Bảng băm (Dict) - Tiêu chuẩn thực tế
# Cấu trúc: Lấy ID làm Key: {1: {"code": "..."}, 2: {"code": "..."}}
# Cách tra cứu: Truy xuất trực tiếp bằng lệnh dict.get(order_id).
# Đánh giá: Siêu nhanh (O(1)). Có 10 triệu đơn thì tra cứu vẫn ra ngay lập tức mà không cần lặp.

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

app = FastAPI()

orders_db = {
    1: {"code": "SP001", "payment_status": "PAID", "method": "BANK_TRANSFER"},
    2: {"code": "SP002", "payment_status": "UNPAID", "method": "NONE"}
}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Hệ thống đang gặp sự cố nội bộ. Vui lòng thử lại sau."}
    )

@app.get("/orders/{order_id}/payment", status_code=status.HTTP_200_OK)
def get_order_payment(order_id: int):
    if order_id < 0:
        trigger_crash = 1 / 0  
        
    order = orders_db.get(order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thông tin đơn hàng."
        )
        
    return {
        "order_id": order_id,
        "payment_status": order["payment_status"],
        "method": order["method"]
    }