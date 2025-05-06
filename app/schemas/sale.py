from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.sale import Sale

class SaleCreate(BaseModel):
    date: Optional[datetime] = None
    totalsale: float = 0.0

class SaleOut(BaseModel):
    id: int
    date: Optional[datetime] = None
    totalsale: float = 0.0


    class Config:
        orm_mode = True