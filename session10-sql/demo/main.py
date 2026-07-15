from fastapi import FastAPI, Depends, Request, status 
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from sqlalchemy.orm import Session
import models
from datetime import datetime
from fastapi.responses import JSONResponse
from database import SessionLocal, engine
from schemas import ResponseAPI

models.Base.metadata.create_all(bind=engine)


class UserCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, description="Không được để trống")
    email: EmailStr


class UserUpdateRequest(BaseModel):
    name: str = Field(..., min_length=2, description="Không được để trống")


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    # Cấu hình này giúp Pydantic đọc được dữ liệu từ SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


class CustomException(Exception):
    def __init__(self, status_code: int, message: str, error: str = None):
        self.status_code = status_code
        self.message = message
        self.error = error



app = FastAPI()


@app.exception_handler(CustomException)
def custom_exception_handle(request: Request, exc: CustomException):
    return JSONResponse(
            status_code= exc.status_code,
            content={
                "status_code": exc.status_code,
                "message": exc.message,
                "data": None,
                "error": exc.error or "Bad Request",
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


@app.get("/")
def read_root():
    return {"message": "Kết nối thành công!"}


@app.get("/users/", response_model= ResponseAPI[list[UserResponse]])
def get_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return ResponseAPI(
        status_code= status.HTTP_200_OK,
        message= "Lay danh sach thanh cong",
        data=users,
        error= None,
        path= request.url.path
    )


@app.post("/users", response_model= ResponseAPI[UserResponse])
def create_user(request: Request,create_user_req: UserCreateRequest, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == create_user_req.email).first()
    if existing_user:
        raise CustomException(
            status_code= status.HTTP_400_BAD_REQUEST,
            message= "email da duoc su dung",
            error= "bad request"
        )

    new_user = models.User(name=create_user_req.name, email=create_user_req.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return ResponseAPI(
        status_code= status.HTTP_201_CREATED,
        message= "Them moi thanh cong",
        data=new_user,
        error= None,
        path= request.url.path
    )


@app.get("/users/{user_id}", response_model= ResponseAPI[UserResponse])
def get_detail_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise CustomException(
            status_code= status.HTTP_404_NOT_FOUND,
            message= "Khong tim thay",
            error= "not found"    
        )

    return ResponseAPI(
        status_code= status.HTTP_200_OK,
        message= "Lay thah cong",
        data= user,
        error= None,
        path= request.url.path
    )

@app.put("/users/{user_id}", response_model=ResponseAPI[UserResponse])
def update_user(user_id: int, request: Request, user_update_req: UserUpdateRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user is None:
        raise CustomException(
            status_code= status.HTTP_404_NOT_FOUND,
            message= "Khong tim thay",
            error= "not found"    
        )
    user.name = user_update_req.name
    db.commit()
    db.refresh(user)

    return ResponseAPI(
        status_code= status.HTTP_200_OK,
        message= "Cap nhat thah cong",
        data= user,
        error= None,
        path= request.url.path
    )

@app.delete("/users/{user_id}", response_model=ResponseAPI[dict])
def delete_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user is None:
        raise CustomException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Không tìm thấy",
            error="not found"    
        )
    
    db.delete(user)
    db.commit()
    
    return ResponseAPI(
        status_code=status.HTTP_200_OK, 
        message="Xóa thành công",
        data=None,
        error=None,
        path=request.url.path
    )