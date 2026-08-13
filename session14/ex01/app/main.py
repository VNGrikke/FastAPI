from fastapi import FastAPI
from app.routers.product import router as product_router
from app.database import engine, Base
import app.models.product

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(product_router)
