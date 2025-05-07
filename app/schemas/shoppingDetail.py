from pydantic import BaseModel
from typing import Optional
from datetime import Date
from app.models.shopping import ShoppingDetail

class ShoppingDetailCreate(BaseModel):
    quantity: Optional[int] = None
    subtotal: Optional[float] = None

class shoppingDetailOut(BaseModel):
    id_shopping_detail: Optional[int] = None
    id_shopping: Optional[int] = None
    id_product: Optional[int] = None
    quantity: Optional[int] = None
    subtotal: Optional[float] = None