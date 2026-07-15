from fastapi import FastAPI, Request, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime
from database import SessionLocal, engine
import models
from pydantic import ConfigDict, BaseModel
from schemas import ResponseAPI
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind = engine)

class CustomException(Exception):
    def __init__(self, status_code: int, message: str, error: str | None):
        self.status_code = status_code
        self.message = message
        self.error = error

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    total_price: int

    model_config = ConfigDict(from_attributes=True)

app = FastAPI()

@app.exception_handler(CustomException)
def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code= exc.status_code,
        content= {
            "status_code" : exc.status_code,
            "message" : exc.message,
            "data": None,
            "error" : exc.error or "Bad request",
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/orders/{order_id}", response_model= ResponseAPI[OrderResponse])
def get_detail_order(order_id: int, request: Request, db : Session = Depends(get_db)):
    order = db.query(models.OrderModel).filter(models.OrderModel.id == order_id).first()
    if order is None:
        raise CustomException(
            status_code= status.HTTP_404_NOT_FOUND,
            message="Khong tim thay don hang",
            error= "Not Found"
        )
    
    return ResponseAPI(
        status_code = status.HTTP_200_OK,
        message= "Da tim thay",
        data= order,
        error= None,
        path= request.url.path
    )


"""
| STT | Phương thức truy vấn hiện tại | Tình huống gây lỗi (Edge Case)                                                                                                                                    | Phương thức thay thế an toàn hơn                                                                                                                                         |
| --- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | `.one()`                      | Khi `order_id = 999` không tồn tại trong bảng `orders`, `.one()` sẽ phát sinh `NoResultFound`, làm API trả về **500 Internal Server Error** nếu không được xử lý. | Dùng `.first()` để trả về `None` nếu không tìm thấy, sau đó kiểm tra và chủ động `raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")`. |

"""