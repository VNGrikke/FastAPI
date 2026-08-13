from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import product as product_service
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from typing import List

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    return product_service.get_products(db)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product_by_id(db, product_id)

@router.post("/", response_model=ProductResponse)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, product_data)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    return product_service.update_product(db, product_id, product_data)

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.delete_product(db, product_id)