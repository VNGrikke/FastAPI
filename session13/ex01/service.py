from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import MenuItem
from schemas import MenuItemCreate, MenuItemUpdate

def get_menu_items(db: Session):
    return db.query(MenuItem).all()

def get_menu_item_by_id(db: Session, item_id: int):
    return db.query(MenuItem).filter(MenuItem.id == item_id).first()

def get_menu_item_by_code(db: Session, dish_code: str):
    return db.query(MenuItem).filter(MenuItem.dish_code == dish_code).first()

def create_menu_item(db: Session, item: MenuItemCreate):
    try:
        db_item = MenuItem(**item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item, None
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)

def update_menu_item(db: Session, db_item: MenuItem, item_data: MenuItemUpdate):
    try:
        update_data = item_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
            
        db.commit()
        db.refresh(db_item)
        return db_item, None
    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)

def delete_menu_item(db: Session, db_item: MenuItem):
    try:
        db.delete(db_item)
        db.commit()
        return True, None
    except SQLAlchemyError as e:
        db.rollback()
        return False, str(e)