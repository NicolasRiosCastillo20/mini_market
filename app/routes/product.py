from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductOut
from app.config.db import get_db
from typing import List


router = APIRouter(prefix='/product', tags=["Product"])


@router.get("/", response_model=List[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.post("/", response_model=ProductOut)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(product=product_data.product, price=product_data.price, stock=product_data.stock)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product