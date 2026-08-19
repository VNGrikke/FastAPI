from sqlalchemy.orm import Session
from fastapi import HTTPException
import models, schemas

def create_warehouse(db: Session, data: schemas.WarehouseCreate):
    try:
        new_warehouse = models.Warehouse(**data.model_dump())
        db.add(new_warehouse)
        db.commit()
        db.refresh(new_warehouse)
        return new_warehouse
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Lỗi tạo nhà kho: {str(e)}")

def get_warehouse_detail(db: Session, warehouse_id: int):
    warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhà kho")
    return warehouse

def update_package(db: Session, package_id: int, data: schemas.PackageUpdate):
    package = db.query(models.Package).filter(models.Package.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Không tìm thấy kiện hàng")
    
    try:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(package, key, value)
            
        db.commit()
        db.refresh(package)
        return package
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Lỗi cập nhật kiện hàng: {str(e)}")

def delete_waybill(db: Session, waybill_id: int):
    waybill = db.query(models.Waybill).filter(models.Waybill.id == waybill_id).first()
    if not waybill:
        raise HTTPException(status_code=404, detail="Không tìm thấy vận đơn")
    
    try:
        db.delete(waybill)
        db.commit()
        return {"message": "Đã xóa vận đơn vĩnh viễn khỏi hệ thống"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Lỗi xóa vận đơn: {str(e)}")