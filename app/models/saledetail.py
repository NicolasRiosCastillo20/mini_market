from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.config.db import Base

class Sale(Base):
    __tablename__ = "saledetail"

    id_detail = Column(Integer, primary_key=True, index=True)
    id_sale = Column(Integer, ForeignKey('sale.id_sale'))
    id_product = Column(Integer, ForeignKey('product.id_product'))
    quantity = Column(Integer)
    price = Column(Float, ForeignKey('product.price'))
    subtotal = Column(Float)

    saledetail = relationship('saledetail', back_populates='products')