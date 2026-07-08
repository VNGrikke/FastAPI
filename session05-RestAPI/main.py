from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

products = [
    {"id": 1, "name" : "sp1", "price": 3000},
    {"id": 2, "name" : "sp2", "price": 1000},
]

class NewProduct(BaseModel):
    id : int
    name : str
    price : int

class UpdateProduct(BaseModel):
    name : str
    price : int


def find_by_id(id):
    for pd in products:
        if pd["id"] == id:
            return pd
        
    return None
 
def is_duplicate(name):
    for pd in products:
        if pd["name"] == name:
            return pd
        
    return None

@app.get("/products")
def get_products():
    return {
        "message" : "Lay danh sach thanh cong",
        "data" : products
    }


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {
                "message" : "Lay san pham thanh cong",
                "data" : product
            }
    return {
        "message" : "Lay san pham khong thanh cong",
        "data" : {}
    }


@app.post("/products")
def create_product(new_product: NewProduct):
    if is_duplicate(new_product.name) :
        return {"message" : "ten san pham da ton tai"}

    products.append(new_product.model_dump())

    return {
        "message" : "Lay danh sach thanh cong",
        "data" : new_product
    }


@app.put("/products/{product_id}")
def update_product(update_product: UpdateProduct, product_id: int):
    product = find_by_id(product_id)
    if product :
        product["name"] = update_product.name
        product["price"] = update_product.price
        return {
            "message": "Cap nhat thanh cong",
            "data": product
        }
    return {
            "message": "Khong tim thay"
    }

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    product = find_by_id(product_id)

    if not product:
        return {
            "message": "Khong tim thay"
        }

    products.remove(product)

    return {
        "message": "Xoa thanh cong",
        "data": product
}


