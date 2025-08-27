from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.config.db import Base

class Supplier(Base):
    __tablename__ = "supplier"

    id_supplier = Column(Integer, primary_key=True, index=True)
    supplier_name = Column(String(255), nullable=False)
    telephone = Column(String(20))
    document_filename = Column(String(255), nullable=True) # Nombre del archivo del documento

    shopping = relationship("Shopping", back_populates="supplier")
    
 
