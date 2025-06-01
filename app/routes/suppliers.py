from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.models.suppliers import Supplier
from app.schemas.suppliers import SupplierCreate, SupplierOut
from app.config.db import get_db
from typing import List

router = APIRouter(prefix='/supplier', tags=['supplier'])


# Llamar proveedores

@router.get('/', response_model=List[SupplierOut])
def get_suppliers(db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).all()
    return suppliers


# crear proveedor

@router.post('/', response_model=SupplierOut)
def create_supplier(supplier_data: SupplierCreate, db: Session = Depends(get_db)):
    new_supplier = Supplier(
        suppliers=supplier_data.suppliers,
        telephone=supplier_data.telephone
    )

    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)

    return new_supplier

# Actualizar proveedor

@router.put('/{supplier_id}', response_model=SupplierOut)
def update_supplier(supplier_id: int, supplier_data: SupplierCreate, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id_supplier == supplier_id).first()

    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")

    supplier.suppliers = supplier_data.suppliers
    supplier.telephone = supplier_data.telephone

    db.commit()
    db.refresh(supplier)

    return supplier

# Eliminar proveedor

@router.delete('/{supplier_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id_supplier == supplier_id).first()

    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")

    db.delete(supplier)
    db.commit()
    return None