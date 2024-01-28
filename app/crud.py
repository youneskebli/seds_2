from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import and_





def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_orders_delivered(db: Session, user_id: int, skip, limit):
    return db.query(models.Order).filter(models.Order.user_id == user_id, models.Order.is_delivered == True).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def create_order(db: Session, order: schemas.OrderCreate, user_id: int, product_id: int):
    db_order = models.Order(**order.dict(), user_id=user_id, product_id=product_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order



def delete_order(db: Session, product_name: str, user_id: int, order_date: str):
    order = db.query(models.Order).join(models.Product).filter(and_(models.Product.product_name == product_name, models.Order.user_id == user_id, models.Order.order_date == order_date)).first()
    if order:
        db.delete(order)
        db.commit()
    return order


 
