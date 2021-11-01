from typing import List, Optional

from pydantic import BaseModel


class DiscountBase(BaseModel):
    code: str
    is_active: bool
    description: Optional[str] = None


class DiscountCreate(DiscountBase):
    pass


class Discount(DiscountBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class BrandBase(BaseModel):
    name: str


class BrandCreate(BrandBase):
    pass


class Brand(BrandBase):
    id: int
    is_active: bool
    discounts: List[Discount] = []

    class Config:
        orm_mode = True
