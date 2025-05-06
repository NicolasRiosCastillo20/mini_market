from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.config.db import Base

class Supplier(Base):
    __tablename__ = "supplier"

    id_supplier = Column(Integer, primary_key=True, index=True)
    suppliers = Column(String(255))
    telephone = Column(String(100))

    # category = relationship("category", back_populates="product")
    # saledetail = relationship('saledetail', back_populates='product')

