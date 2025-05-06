from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.config.db import Base

class Sale(Base):
    __tablename__ = "sale"

    id_sale = Column(Integer, primary_key=True, index=True)
    datesale = Column(DateTime, onupdate=datetime.timezone.utcnow())
    totalsale = Column(Float)

    sale = relationship('sale', back_populates='saledetail')