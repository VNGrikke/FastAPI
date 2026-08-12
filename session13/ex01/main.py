from fastapi import FastAPI
from router import router as product_router 

app = FastAPI()

app.include_router(product_router)

