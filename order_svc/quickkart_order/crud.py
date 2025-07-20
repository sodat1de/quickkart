from sqlalchemy.orm import Session

from . import models, schemas


def create_order(db: Session, user_email: str, order_in: schemas.OrderCreate):
    order = models.Order(user_email=user_email, item=order_in.item)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def list_orders(db: Session, user_email: str):
    return db.query(models.Order).filter(models.Order.user_email == user_email).all()
