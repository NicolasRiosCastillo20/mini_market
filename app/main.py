from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes import user,product,category, sale, shopping, suppliers
from app.config.db import Base, engine


app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

# Configuración de la ruta para la página de inicio

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "title": "Home Page"})

@app.get("/ventas.html", response_class=HTMLResponse)
async def ventas(request: Request):
    return templates.TemplateResponse("ventas.html", {"request": request, "title": "Ventas"})


# @app.get("/", response_class=HTMLResponse)
# async def login_get(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})

# @app.post("/")
# async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
#     if username == "admin" and password == "1234":  # ← aquí iría tu lógica real
#         return RedirectResponse("/", status_code=303)
#     else:
#         return templates.TemplateResponse("login.html", {
#             "request": request,
#             "error": "Credenciales incorrectas"
#         })


# Crear las tablas
Base.metadata.create_all(bind=engine)

#registrar rutas

app.include_router(user.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(sale.router)
app.include_router(shopping.router)
app.include_router(suppliers.router)






