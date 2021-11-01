import random
import string
from sqlalchemy.orm import Session

import models, schemas


def get_brand(db: Session, brand_id: int):
    return db.query(models.Brand).filter(models.Brand.id == brand_id).first()


def get_brand_by_name(db: Session, name: str):
    return db.query(models.Brand).filter(models.Brand.name == name).first()


def get_brands(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Brand).offset(skip).limit(limit).all()


def create_brand(db: Session, brand: schemas.BrandCreate):
    db_brand = models.Brand(name=brand.name)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand


def get_discounts_by_brand(db: Session,
                           brand_id: int,
                           skip: int = 0,
                           limit: int = 100):
    db_brand = get_brand(db, brand_id)
    return db.query(
        models.Discount).filter(models.Discount.owner_id ==
                                db_brand.id).offset(skip).limit(limit).all()


def get_discounts_by_brand_name(db: Session,
                                brand_name: str,
                                active: bool = True,
                                skip: int = 0,
                                limit: int = 100):
    db_brand = get_brand_by_name(db, brand_name)
    return db.query(models.Discount).filter(
        models.Discount.owner_id == db_brand.id).filter(
            models.Discount.is_active == active).offset(skip).limit(
                limit).all()


def get_active_discounts_by_brand(db: Session,
                                  brand_id: int,
                                  skip: int = 0,
                                  limit: int = 100):
    db_brand = get_brand(db, brand_id)
    return db.query(models.Discount).filter(
        models.Discount.owner_id == db_brand.id).filter(
            models.Discount.is_active == True).offset(skip).limit(limit).all()


def get_discount(db: Session, brand_id: int):
    active_discounts = get_active_discounts_by_brand(db, brand_id)
    if len(active_discounts) > 0:
        discount = active_discounts[0]
        discount.is_active = False
        db.commit()
    else:
        discount = None
    return discount


def get_discounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Discount).offset(skip).limit(limit).all()


def create_brand_discounts(db: Session,
                           number: int,
                           brand_id: int,
                           length: int = 8):
    db_brand = get_brand(db, brand_id)
    for i in range(number):
        code = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=length))
        description = f"Use the following code to get a discount with {db_brand.name}"
        db_discount = models.Discount(code=code,
                                      description=description,
                                      is_active=True,
                                      owner_id=brand_id)
        db.add(db_discount)
        db.commit()
    db.refresh(db_discount)
    return f"Successfully generated {number} discount codes for {db_brand.name}."
