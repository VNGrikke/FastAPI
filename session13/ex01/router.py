from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas, service

router = APIRouter(prefix="/menu-items", tags=["Menu Items"])

# 1. Thêm món ăn mới (POST)
@router.post("", response_model=schemas.StandardResponse[schemas.MenuItemResponse])
def create_item(request: Request, response: Response, item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    # Check trùng lặp mã món
    if service.get_menu_item_by_code(db, item.dish_code):
        response.status_code = 400
        return schemas.StandardResponse(
            statusCode=400, message="Thêm món ăn thất bại", error="Mã món ăn đã tồn tại", data=None, path=request.url.path
        )
    
    new_item, err = service.create_menu_item(db, item)
    if err:
        response.status_code = 500
        return schemas.StandardResponse(
            statusCode=500, message="Lỗi hệ thống CSDL", error=err, data=None, path=request.url.path
        )

    response.status_code = 201
    return schemas.StandardResponse(
        statusCode=201, message="Thêm món ăn thành công", data=new_item, path=request.url.path
    )

# 2. Lấy danh sách toàn bộ món ăn (GET)
@router.get("", response_model=schemas.StandardResponse[List[schemas.MenuItemResponse]])
def get_all_items(request: Request, db: Session = Depends(get_db)):
    items = service.get_menu_items(db)
    return schemas.StandardResponse(
        statusCode=200, message="Lấy danh sách thành công", data=items, path=request.url.path
    )

# 3. Lấy thông tin chi tiết một món ăn (GET)
@router.get("/{item_id}", response_model=schemas.StandardResponse[schemas.MenuItemResponse])
def get_item_detail(request: Request, response: Response, item_id: int, db: Session = Depends(get_db)):
    item = service.get_menu_item_by_id(db, item_id)
    if not item:
        response.status_code = 404
        return schemas.StandardResponse(
            statusCode=404, message="Menu item not found", error="Not Found", data=None, path=request.url.path
        )
        
    return schemas.StandardResponse(
        statusCode=200, message="Lấy chi tiết món ăn thành công", data=item, path=request.url.path
    )

# 4. Cập nhật thông tin món ăn (PUT)
@router.put("/{item_id}", response_model=schemas.StandardResponse[schemas.MenuItemResponse])
def update_item(request: Request, response: Response, item_id: int, item_data: schemas.MenuItemUpdate, db: Session = Depends(get_db)):
    db_item = service.get_menu_item_by_id(db, item_id)
    if not db_item:
        response.status_code = 404
        return schemas.StandardResponse(
            statusCode=404, message="Menu item not found", error="Not Found", data=None, path=request.url.path
        )

    if item_data.dish_code and item_data.dish_code != db_item.dish_code:
        if service.get_menu_item_by_code(db, item_data.dish_code):
            response.status_code = 400
            return schemas.StandardResponse(
                statusCode=400, message="Cập nhật thất bại", error="Mã món ăn đã tồn tại", data=None, path=request.url.path
            )
            
    updated_item, err = service.update_menu_item(db, db_item, item_data)
    if err:
        response.status_code = 500
        return schemas.StandardResponse(
            statusCode=500, message="Lỗi hệ thống CSDL", error=err, data=None, path=request.url.path
        )

    return schemas.StandardResponse(
        statusCode=200, message="Cập nhật món ăn thành công", data=updated_item, path=request.url.path
    )

@router.delete("/{item_id}", response_model=schemas.StandardResponse)
def delete_item(request: Request, response: Response, item_id: int, db: Session = Depends(get_db)):
    db_item = service.get_menu_item_by_id(db, item_id)
    if not db_item:
        response.status_code = 404
        return schemas.StandardResponse(
            statusCode=404, message="Menu item not found", error="Not Found", data=None, path=request.url.path
        )
        
    success, err = service.delete_menu_item(db, db_item)
    if err:
        response.status_code = 500
        return schemas.StandardResponse(
            statusCode=500, message="Lỗi hệ thống CSDL", error=err, data=None, path=request.url.path
        )
        
    return schemas.StandardResponse(
        statusCode=200, message="Xóa món ăn thành công", data=None, path=request.url.path
    )