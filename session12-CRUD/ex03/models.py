from sqlalchemy import Column, String, Integer
from database import Base

class ShipmentModel(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_code = Column(String(50), unique=True, nullable=False)
    receiver_name = Column(String(100), nullable=False)
    delivery_address = Column(String(255), nullable=False)