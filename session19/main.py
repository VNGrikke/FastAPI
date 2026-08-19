from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import schemas, service

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Logistics Management API")

@app.post("/warehouses", response_model=schemas.WarehouseDetailResponse, status_code=status.HTTP_201_CREATED)
def create_warehouse_endpoint(warehouse: schemas.WarehouseCreate, db: Session = Depends(get_db)):
    return service.create_warehouse(db, warehouse)

@app.get("/warehouses/{warehouse_id}", response_model=schemas.WarehouseDetailResponse, status_code=status.HTTP_200_OK)
def get_warehouse_endpoint(warehouse_id: int, db: Session = Depends(get_db)):
    return service.get_warehouse_detail(db, warehouse_id)

@app.patch("/packages/{package_id}", response_model=schemas.PackageResponse, status_code=status.HTTP_200_OK)
def update_package_endpoint(package_id: int, package: schemas.PackageUpdate, db: Session = Depends(get_db)):
    return service.update_package(db, package_id, package)

@app.delete("/waybills/{waybill_id}", status_code=status.HTTP_200_OK)
def delete_waybill_endpoint(waybill_id: int, db: Session = Depends(get_db)):
    return service.delete_waybill(db, waybill_id)