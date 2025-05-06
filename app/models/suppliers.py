from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.config.db import Base

class Supplier(Base):
    __tablename__ = "supplier"

    id_supplier = Column(Integer, primary_key=True, index=True)
    suppliers = Column(String(255))
    telephone = Column(String(100))
# se borran 2 lineas de código

