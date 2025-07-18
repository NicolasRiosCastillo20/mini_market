from fastapi import APIRouter, Depends, HTTPException, status, Request, Form, File, UploadFile, Query
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.models import Supplier, Shopping, ShoppingDetail, Product
from app.models.category import Category
from app.schemas.suppliers import SupplierCreate, SupplierOut
from app.config.db import get_db
import os
import shutil
from uuid import uuid4

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")  # Ajusta si tu ruta real es diferente

# =========================
# Obtener lista de proveedores
# =========================
@router.get('/', response_model=List[SupplierOut])
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()

@router.get("/supplier/search")
def buscar_proveedor(name: str = Query(...), db: Session = Depends(get_db)):
    proveedor = db.query(Supplier).filter(Supplier.supplier_name == name).first()

    if not proveedor:
        return {"success": False, "message": f"Proveedor '{name}' no encontrado"}

    return {
        "success": True,
        "supplier": {
            "name": proveedor.supplier_name,
            "phone": proveedor.telephone
        },
        "files": []  # Puedes agregar aquí lógica si manejas archivos PDF
    }

# =========================
# Crear proveedor
# =========================
UPLOAD_FOLDER = "uploaded_files"  # puedes cambiar esta ruta

@router.post("/ingresos/supplier/create")
async def crear_supplier(
    supplierName: str = Form(...),
    supplierPhone: str = Form(...),
    supplierDocument: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    nuevo_proveedor = Supplier(supplier_name=supplierName, telephone=supplierPhone)
    db.add(nuevo_proveedor)
    db.commit()
    db.refresh(nuevo_proveedor)

    if supplierDocument and supplierDocument.filename:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        extension = os.path.splitext(supplierDocument.filename)[1]
        nuevo_nombre = f"{uuid4().hex}_{nuevo_proveedor.id_supplier}{extension}"
        ruta_archivo = os.path.join(UPLOAD_FOLDER, nuevo_nombre)
        with open(ruta_archivo, "wb") as buffer:
            shutil.copyfileobj(supplierDocument.file, buffer)

    return RedirectResponse(url="/category/proveedores", status_code=303)

# =========================
# Actualizar proveedor
# =========================
@router.put('/{supplier_id}', response_model=SupplierOut)
def update_supplier(supplier_id: int, supplier_data: SupplierCreate, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id_supplier == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")

    supplier.supplier_name = supplier_data.supplier_name
    supplier.telephone = supplier_data.telephone

    db.commit()
    db.refresh(supplier)
    return supplier

# =========================
# Eliminar proveedor
# =========================
@router.delete('/{supplier_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id_supplier == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado")

    db.delete(supplier)
    db.commit()
    return None

# =========================
# Mostrar formulario ingreso
# =========================
@router.get("/formulario")
def mostrar_formulario_ingreso(request: Request, db: Session = Depends(get_db)):
    proveedores = db.query(Supplier).all()
    categorias = db.query(Category).all()
    return templates.TemplateResponse("productos.html", {  # <- Aquí cambió el nombre
        "request": request,
        "proveedores": proveedores,
        "categorias": categorias
    })

# =========================
# Registrar ingreso POST
# =========================
@router.post("/registrar")
def registrar_ingreso(
    fecha_ingreso: str = Form(...),
    proveedor_nombre: str = Form(...),
    productos: list[str] = Form(...),
    cantidades: list[int] = Form(...),
    precios: list[float] = Form(...),
    precio_venta: list[float] = Form(...),
    categorias: list[str] = Form(...),
    db: Session = Depends(get_db)
):
    proveedor = db.query(Supplier).filter(Supplier.supplier_name == proveedor_nombre).first()
    if not proveedor:
        proveedor = Supplier(supplier_name=proveedor_nombre)
        db.add(proveedor)
        db.commit()
        db.refresh(proveedor)

    total_shopping = 0.0
    nuevo_ingreso = Shopping(
        shopping_date=fecha_ingreso,
        id_supplier=proveedor.id_supplier,
        total_shopping=0.0
    )
    db.add(nuevo_ingreso)
    db.commit()
    db.refresh(nuevo_ingreso)

    for nombre, cantidad, precio_compra, precio_venta_unitario, nombre_categoria in zip(productos, cantidades, precios, precio_venta, categorias):
        total_shopping += cantidad * precio_compra

        categoria = db.query(Category).filter(Category.category == nombre_categoria).first()
        if not categoria:
            categoria = Category(category=nombre_categoria)
            db.add(categoria)
            db.commit()
            db.refresh(categoria)

        producto = Product(
            product=nombre,
            stock=cantidad,
            shopping_price=precio_compra,
            sale_price=precio_venta_unitario,
            id_shopping=nuevo_ingreso.id_shopping,
            id_category=categoria.id_category
        )
        db.add(producto)
        db.commit()
        db.refresh(producto)

        detalle = ShoppingDetail(
            id_shopping=nuevo_ingreso.id_shopping,
            id_product=producto.id_product,
            quantity=cantidad,
            subtotal=precio_compra * cantidad
        )
        db.add(detalle)

    nuevo_ingreso.total_shopping = total_shopping
    db.commit()

    return RedirectResponse(url="/productos", status_code=303)
