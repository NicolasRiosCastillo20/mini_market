from pydantic import BaseModel

class ProductCreate(BaseModel):
    product: str
    price: float
    stock: int
    id_category: int

class ProductOut(BaseModel):
    id: int
    product: str
    price: float
    stock: int
    id_category: int


    class Config:
        orm_mode = True