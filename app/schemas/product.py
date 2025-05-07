from pydantic import BaseModel

class ProductCreate(BaseModel):
    product: str
    shopping_price: float
    sale_price: float
    stock: int
    id_category: int

class ProductOut(BaseModel):
    id_product: int
    product: str
    shopping_price: float
    sale_price: float
    stock: int
    id_category: int

    class Config:
        orm_mode = True