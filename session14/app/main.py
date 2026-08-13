from fastapi import FastAPI
from router.product import router as product_router 

app = FastAPI()

app.include_router(product_router)