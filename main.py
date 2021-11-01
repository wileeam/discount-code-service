from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Get discount code service",
    description="A simple API service to generate discount codes and retrieve them.",
    version="0.0.1",
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/brand/", response_model=schemas.Brand)
def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
    db_brand = crud.get_brand_by_name(db, name=brand.name)
    if db_brand:
        raise HTTPException(status_code=400, detail="Brand already exists.")

    return crud.create_brand(db=db, brand=brand)


@app.get("/brand/all", response_model=List[schemas.Brand])
def get_all_brands(skip: int = 0,
                   limit: int = 100,
                   db: Session = Depends(get_db)):
    brands = crud.get_brands(db, skip=skip, limit=limit)

    return brands


@app.get("/brand/{brand_id}", response_model=schemas.Brand)
def get_brand(brand_id: int, db: Session = Depends(get_db)):
    db_brand = crud.get_brand(db, brand_id=brand_id)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Sorry, brand not found.")
    return db_brand


@app.post("/brand/{brand_id}/discounts/{number}")
def create_discount_for_brand(brand_id: int,
                              number: int,
                              discount: schemas.DiscountCreate,
                              db: Session = Depends(get_db)):

    return crud.create_brand_discounts(db=db, number=number, brand_id=brand_id)


@app.get("/discount/{brand_id}", response_model=schemas.Discount)
def get_discount_for_brand(brand_id: int, db: Session = Depends(get_db)):

    discount = crud.get_discount(db, brand_id=brand_id)
    if discount:
        discount.is_active = False

    return discount


@app.get("/discounts/{brand_id}/all", response_model=List[schemas.Discount])
def get_discounts_for_brand(brand_id: int,
                            skip: int = 0,
                            limit: int = 100,
                            db: Session = Depends(get_db)):
    discounts = crud.get_discounts_by_brand(db,
                                            brand_id=brand_id,
                                            skip=skip,
                                            limit=limit)

    return discounts


@app.get("/discounts/{brand_id}/active", response_model=List[schemas.Discount])
def get_active_discounts_for_brand(brand_id: int,
                                   skip: int = 0,
                                   limit: int = 100,
                                   db: Session = Depends(get_db)):
    discounts = crud.get_active_discounts_by_brand(db,
                                                   brand_id=brand_id,
                                                   skip=skip,
                                                   limit=limit)

    return discounts


@app.get("/discounts/all", response_model=List[schemas.Discount])
def get_all_discounts(skip: int = 0,
                      limit: int = 100,
                      db: Session = Depends(get_db)):
    discounts = crud.get_discounts(db, skip=skip, limit=limit)

    return discounts
