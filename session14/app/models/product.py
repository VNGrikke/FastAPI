from sqlalchemy import Column, Integer, Float, String
from app.database.database import Base
class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    