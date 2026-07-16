import models
from fastapi import HTTPException
def get_all_pd(db):
    products = db.query(models.Product).all()
    return {
        "data" : products
    }

def get_detail(db, id):
    pd = db.query(models.Product).filter(models.Product.id == id).first()
    if pd is None:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay sp"
        )
    
    return {
        "message" : "TIm thay",
        "data" : pd
    }