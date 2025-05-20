from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.models.shopping import Shopping
from app.schemas.shopping import ShoppingCreate, ShoppingOut, ShoppingFull
from app.models.shoppingDetail import ShoppingDetail
from app.models.product import Product
from app.config.db import get_db
from typing import List

router = APIRouter(prefix='/shopping', tags=['shopping'])

@router.get('/', response_model=List[ShoppingOut])
def get_shoppings(db:Session = Depends(get_db)):
    return db.query(Shopping).all()


@router.post('/', response_model=ShoppingOut)
def create_shopping(shopping_data:ShoppingCreate, db:Session = Depends(get_db)):
    new_shopping = Shopping(
        id_supplier = 1,
        shopping_date = shopping_data.shopping_date,
        total_shopping = shopping_data.total_shopping
    )

    db.add(new_shopping)
    db.commit()
    db.refresh(new_shopping)

    total = 0.0

    for detail in shopping_data.details:
        product =  db.query(Product).filter(Product.id_product == detail.id_product).first()

        if not product:
            raise ValueError(f"Producto con id {detail.id_product} no existe")
        
        subtotal = product.shopping_price * detail.quantity
        total += subtotal

        product.stock += detail.quantity
        db.commit()
        db.refresh(product)


        new_detail = ShoppingDetail(
            id_shopping = new_shopping.id_shopping,
            id_product = detail.id_product,
            quantity = detail.quantity,
            subtotal = subtotal
        )

        db.add(new_detail)

    new_shopping.total_shopping = total
    db.commit()
    db.refresh(new_shopping)
    
    return new_shopping


