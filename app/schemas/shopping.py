from pydantic import BaseModel
from typing import Optional
from datetime import Date
from app.models.shopping import Shopping

class ShoppingCreate(BaseModel):
    Shopping_date: Optional[Date] = None
    total_shopping: Optional[float] = None

class ShoppingOut(BaseModel):
    id_shopping: int
    id_supplier: int
    Shopping_date: Optional[Date] = None
    total_shopping: float

    class Config:
        orm_mode = True