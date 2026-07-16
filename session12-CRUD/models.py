from sqlalchemy import Column, String, Integer
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    price = Column(Integer, index=True)