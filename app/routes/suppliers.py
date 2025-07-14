from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from app.models.suppliers import Supplier
from app.models import Supplier, Shopping, ShoppingDetail, Product

from datetime import datetime   
from app.schemas.suppliers import SupplierCreate, SupplierOut
from app.config.db import get_db
from typing import List

router = APIRouter(prefix='/supplier', tags=['supplier'])
router = APIRouter(prefix='/ingresos')

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


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

@router.post("/registrar")
def registrar_ingreso(
    fecha_ingreso: str = Form(...),
    proveedor_nombre: str = Form(...),
    productos: list[str] = Form(...),
    cantidades: list[int] = Form(...),
    precios: list[float] = Form(...),
    precio_venta: list[float] = Form(...),
    db: Session = Depends(get_db)
):
    proveedor = db.query(Supplier).filter(Supplier.suppliers == proveedor_nombre).first()
    if not proveedor:
        proveedor = Supplier(suppliers=proveedor_nombre)
        db.add(proveedor)
        db.commit()
        db.refresh(proveedor)

    # Crear ingreso (Shopping)
    total_shopping = 0.0
    nuevo_ingreso = Shopping(shopping_date=fecha_ingreso, id_supplier=proveedor.id_supplier, total_shopping=0.0)
    db.add(nuevo_ingreso)
    db.commit()
    db.refresh(nuevo_ingreso)

    # Agregar productos
    for nombre, cantidad, precio_compra, precio_venta_unitario in zip(productos, cantidades, precios, precio_venta):
        total_shopping += cantidad * precio_compra  # Sumar al total

        producto = Product(
            product=nombre,
            stock=cantidad,
            shopping_price=precio_compra,
            sale_price=precio_venta_unitario,
            id_shopping=nuevo_ingreso.id_shopping
        )
        db.add(producto)

    # Actualizar total_shopping
    nuevo_ingreso.total_shopping = total_shopping
    db.commit()

    entrada = Shopping(shopping_date=datetime.strptime(fecha_ingreso, "%Y-%m-%d"), id_supplier=proveedor.id_supplier)
    db.add(entrada)
    db.commit()
    db.refresh(entrada)

    for nombre, cantidad, precio, p_venta in zip(productos, cantidades, precios, precio_venta):
        producto = db.query(Product).filter(Product.product == nombre).first()
        if not producto:
            producto = Product(
                product=nombre,
                stock=cantidad,  # ✅ aquí usamos solo la cantidad de este producto
                sale_price=p_venta,
                shopping_price=precio
            )
            db.add(producto)
            db.commit()
            db.refresh(producto)
        else:
            producto.stock += cantidad
            producto.shopping_price = precio
            producto.sale_price = p_venta
            db.commit()

        detalle = ShoppingDetail(
            id_shopping=entrada.id_shopping,
            id_product=producto.id_product,
            quantity=cantidad,
            subtotal=precio
        )
        db.add(detalle)

    db.commit()

    return RedirectResponse(url="/productos", status_code=303)
