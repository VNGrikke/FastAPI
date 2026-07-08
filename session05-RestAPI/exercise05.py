from fastapi import FastAPI

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "is_active": True},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "is_active": True},
    {"id": 3, "code": "SP003", "name": "Monitor", "price": 2500000, "is_active": False}
]

app = FastAPI()

def find_product_by_id(id):
    for pd in products:
        if pd["id"] == id:
            return pd
        
    return None


@app.patch("/products/{product_id}")
def deactive_product(product_id:int):
    product = find_product_by_id(product_id)

    if product is None:
        return {"message" : "Product not found"}

    if product["is_active"] == False:
        return {"message" : "Product already inactive"}

    product["is_active"] = False

    return {"message" : "Ngừng kinh doanh thành công"}