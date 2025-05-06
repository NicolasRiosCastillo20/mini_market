from sqlalchemy import Column, Integer, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from app.config.db import Base

class Shopping(Base):
    __tablename__ = "shopping"
    
    id_shopping = Column(Integer, primary_key=True, index=True)
    id_supplier = Column(Integer, ForeignKey("supplier.id_supplier"))
    shopping_date = Column(Date)
    total_shopping = Column(Float)

    supplier = relationship("suppliers", back_populates="shopping")
