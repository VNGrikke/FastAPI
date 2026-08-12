from database import Base, engine
from sqlalchemy import Column, Integer, Float, String
import models

models.Base.metadata.create_all(engine)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable= False)
    price = Column(Float, nullable=False)