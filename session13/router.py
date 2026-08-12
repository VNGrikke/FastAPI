from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from service import get_all_product,get_product, create_product, update_product, del_product
from schemas import CreateProductReq, UpdateProductReq

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("")
def get_products(db: Session = Depends(get_db)):
    return {
        "message": "da lay",
        "data": get_all_product(db)
    }

@router.get("/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    return {
        "message": "da lay",
        "data": get_product(id, db) 
    }

@router.post("")
def post_product(create_product_req: CreateProductReq, db: Session = Depends(get_db)):

    return {
        "message": "Them moi thanh cong",
        "data": create_product(create_product_req,db)
    }

@router.put("/{id}")
def put_product(id: int, update_product_req: UpdateProductReq, db: Session = Depends(get_db)):

     return {
        "message": "Cap nhat moi thanh cong",
        "data": update_product(id, update_product_req,db)
    }

@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):

    return {
        "message": "Xoa thanh cong",
        "data": del_product(id, db)
    }