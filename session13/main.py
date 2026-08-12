from fastapi import FastAPI
from router import router as product_router 

app = FastAPI()

app.include_router(product_router)

@app.get("/")
def test_api():
    return {"message": "API dang chay"}