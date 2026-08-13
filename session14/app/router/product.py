from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from services.product import get_products

router = APIRouter(
    prefix= "/products",
    tags=["Product"]
)

@router.get("")
def get_all_product(db: Session = Depends(get_db)):
    return get_products(db)