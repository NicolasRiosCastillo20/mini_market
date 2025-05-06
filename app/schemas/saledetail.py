from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.sale import Sale

class SaleDetailCreate(BaseModel):
    id_sale: Optional[int] = None
    id_product: Optional[int] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    subtotal: Optional[float] = None

class SaleDetailOut(BaseModel):
    id_sale: int
    id_product: int
    quantity: int
    price: float
    subtotal: float


    class Config:
        orm_mode = True