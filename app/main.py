from fastapi import FastAPI
from app.routes import user
from app.config.db import Base, engine

app = FastAPI()

# Crear las tablas
Base.metadata.create_all(bind=engine)

#registrar rutas
app.include_router(user.router)




