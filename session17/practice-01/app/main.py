from fastapi import FastAPI
from app.routers.classroom import router_classroom
from app.routers.student import router_student
from app.database.database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(router_classroom)
app.include_router(router_student)

@app.get("/")
def test():
    return {"message": "Chay thanh cong"}