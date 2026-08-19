from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)

    # Quan hệ 1-N: 1 nhà kho có nhiều kiện hàng
    packages = relationship("Package", back_populates="warehouse")

class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    package_code = Column(String(50), unique=True, index=True, nullable=False)
    weight = Column(Float, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)

    warehouse = relationship("Warehouse", back_populates="packages")
    # Quan hệ 1-1: 1 kiện hàng có 1 vận đơn
    waybill = relationship("Waybill", back_populates="package", uselist=False)

class Waybill(Base):
    __tablename__ = "waybills"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(50), unique=True, index=True, nullable=False)
    shipping_status = Column(String(50), nullable=False)
    # Ràng buộc unique=True đảm bảo 1 vận đơn chỉ thuộc về 1 kiện hàng
    package_id = Column(Integer, ForeignKey("packages.id"), unique=True, nullable=False)

    package = relationship("Package", back_populates="waybill")