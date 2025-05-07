from pydantic import BaseModel
from datetime import Date
from app.models.suppliers import Supplier

class SupplierCreate(BaseModel):
    suppliers: str
    telephone: str

class SupplierOut(BaseModel):
    id_supplier: int
    suppliers: str
    telephone: str

    class Config:
        orm_mode = True