from pydantic import BaseModel
from typing import Optional
from datetime import date
from .shoppingDetail import ShoppingDetailCreate, ShoppingDetailOut

class ShoppingCreate(BaseModel):
    shopping_date: Optional[date] = None
    total_shopping: float
    details: list[ShoppingDetailCreate]

class ShoppingOut(BaseModel):
    id_shopping: int
    id_supplier: int
    shopping_date: Optional[date] = None
    total_shopping: float

    class Config:
        orm_mode = True

class ShoppingFull(ShoppingOut):
    details: list[ShoppingDetailOut]