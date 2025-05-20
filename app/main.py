from fastapi import FastAPI
from app.routes import user,product,category, sale, shopping
from app.config.db import Base, engine

app = FastAPI()

# Crear las tablas
Base.metadata.create_all(bind=engine)

#registrar rutas
app.include_router(user.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(sale.router)
app.include_router(shopping.router)




