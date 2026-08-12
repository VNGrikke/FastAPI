import models
from database import engine, Base
from schemas import CreateProductReq, UpdateProductReq
from fastapi import HTTPException

models.Base.metadata.create_all(bind=engine)

def get_all_product(db):
    return db.query(models.Product).all()

def get_product(id: int, db):
    return db.query(models.Product).filter(models.Product.id == id).first()

def create_product(create_product_req: CreateProductReq, db):
    existing_product = db.query(models.Product).filter(models.Product.name == create_product_req.name).first()

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="Ten da ton tai"
        )
    
    new_product = models.Product(name=create_product_req.name, price=create_product_req.price)

    db.add(new_product) 
    
    db.commit()
    db.refresh(new_product)

    return new_product

def update_product(id: int, update_product_req: UpdateProductReq, db):
    product = get_product(id, db)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay"
        )
    
    if update_product_req.name is not None:
        product.name = update_product_req.name

    if update_product_req.price is not None:
        product.price = update_product_req.price

    db.commit()
    db.refresh(product)

    return product
    
def del_product(id: int, db):
    product = get_product(id, db)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay"
        )
    
    db.delete(product)
    db.commit()

    return None