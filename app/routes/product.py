from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductOut
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut
from app.config.db import get_db
from typing import List


router = APIRouter(prefix='/product', tags=["Product"])


@router.get("/", response_model=List[ProductOut])
def get_product(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.post("/", response_model=ProductOut)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(product=product_data.product, price=product_data.price, stock=product_data.stock)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

# prueba category

@router.get("/category", response_model=List[CategoryOut])
def get_category(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.post("/category", response_model=CategoryOut)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(product=category_data.category)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
