from database.database import get_db
from models.product import Product

def get_products(db):
    products = db.query(Product).all()
    return{
        "message": "Lay adnh sahc san phm",
        "data": products
    }