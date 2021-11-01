from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    discounts = relationship("Discount", back_populates="owner")


class Discount(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    description = Column(String, index=True)
    is_active = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("brands.id"))

    owner = relationship("Brand", back_populates="discounts")
