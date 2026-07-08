from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, Tuple, Dict, Any

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5}
]

class ProductUpdate(BaseModel):
    code: str
    name: str = Field(..., min_length=1, strip_whitespace=True) 
    price: float = Field(..., gt=0)                             
    stock: int = Field(..., ge=0)                               

def validate_and_find_index(product_id: int, new_code: str) -> Tuple[Optional[Dict[str, str]], Optional[int]]:
    target_index = None
    
    for i, p in enumerate(products):
        if p["code"] == new_code and p["id"] != product_id:
            return {"detail": "Product code already exists"}, None
            
        if p["id"] == product_id:
            target_index = i
            
    if target_index is None:
        return {"detail": "Product not found"}, None
        
    return None, target_index

@app.put("/products/{product_id}")
async def update_product(product_id: int, payload: ProductUpdate):
    
    error, target_index = validate_and_find_index(product_id, payload.code)
    
    if error:
        return error

    updated_data = {"id": product_id, **payload.model_dump()}
    products[target_index] = updated_data
    
    return updated_data