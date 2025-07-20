from sqlalchemy.orm import Session

from . import models, schemas


def create_product(db: Session, product_in: schemas.ProductCreate):
    product = models.Product(**product_in.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def list_products(db: Session):
    return db.query(models.Product).all()