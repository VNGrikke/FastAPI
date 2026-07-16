from fastapi import Depends, FastAPI
from database import SessionLocal, engine
import models
from sqlalchemy.orm import Session
from service import get_all_pd,get_detail
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/")
def home():
    return {
        "message" : "API dang chay"
    }


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return get_all_pd(db)

@app.get("/products/{id_pd}")
def get_dt_pd( id_pd: int, db: Session = Depends(get_db)):
    return get_detail(db, id_pd)


