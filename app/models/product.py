from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.config.db import Base

class Product(Base):
    __tablename__ = "product"

    id_product = Column(Integer, primary_key=True, index=True)
    product = Column(String(100))
    shopping_price = Column(Float)
    sale_price = Column(Float)
    stock = Column(Integer)
    id_category = Column(Integer, ForeignKey('category.id_category'))

    category = relationship("category", back_populates="product")
    saledetail = relationship('saledetail', back_populates='product')


