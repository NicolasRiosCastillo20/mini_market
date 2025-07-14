from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.config.db import Base

class Supplier(Base):
    __tablename__ = "supplier"

    id_supplier = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    telephone = Column(String(100))

    shopping = relationship("Shopping", back_populates="supplier")
    
 
