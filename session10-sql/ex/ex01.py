from fastapi import FastAPI, Request, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime
from database import SessionLocal, engine
import models
from pydantic import BaseModel, ConfigDict, Field
from schemas import ResponseAPI
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind = engine)

class CustomException(Exception):
    def __init__(self, status_code: int, message: str, error: str|None):
        self.status_code = status_code
        self.message = message
        self.error = error

class ProductResponse(BaseModel):
    id: int
    sku: str 
    name: str
    price: float

    model_config = ConfigDict(from_attributes=True)

class ProductCreateRequest(BaseModel):
    sku: str = Field(..., max_length=50, description="Khong dc de trong")
    name: str = Field(..., max_length=255, description="Khong duoc de trong")
    price: float = Field(..., gt=0, description="Nhap 1 so thuc lon hon 0")

app = FastAPI()

@app.exception_handler(CustomException)
def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code= exc.status_code,
        content={
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


@app.post("/products", response_model= ResponseAPI[ProductResponse])
def create_product(request: Request, pd_cr_req: ProductCreateRequest, db: Session = Depends(get_db)):
    existing_product = db.query(models.ProductModel).filter(models.ProductModel.sku == pd_cr_req.sku).first()

    if existing_product:
        raise CustomException(
            status_code= status.HTTP_400_BAD_REQUEST,
            message= "sku(sku la cai gi????) da ton tai",
            error= "Bad request"
        )


    new_pd = models.ProductModel(sku = pd_cr_req.sku, name = pd_cr_req.name, price = pd_cr_req.price)

    db.add(new_pd)
    db.commit()
    db.refresh(new_pd)

    return ResponseAPI(
        status_code = status.HTTP_201_CREATED,
        message = "Them san pham thanh cong",
        data= new_pd,
        error = None,
        path = request.url.path
    )

"""
| STT | Hành vi lỗi trong code hiện tại                                           | Hậu quả đối với Database MySQL                                                                                                      | Cách khắc phục bằng SQLAlchemy                                                                                        |
| --- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 1   | Thiếu lệnh xác thực lưu dữ liệu (`db.commit()`) sau `db.add(new_product)` | Dữ liệu chỉ nằm trong Session, không được ghi xuống bảng `products`. API trả về thành công nhưng database vẫn không có bản ghi nào. | Gọi `db.commit()` sau `db.add(new_product)` và nên gọi thêm `db.refresh(new_product)` để đồng bộ dữ liệu từ database. |
| 2   | Không giải phóng/đóng Session (`db.close()`)                              | Connection không được trả về connection pool, dễ gây rò rỉ kết nối (connection leak), làm cạn pool khi có nhiều request đồng thời.  | Đóng Session bằng `db.close()` trong khối `finally` để đảm bảo luôn giải phóng kết nối, kể cả khi xảy ra lỗi.         |

"""