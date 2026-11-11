from fastapi import FastAPI

from routers import categorias, productos


app = FastAPI(
    title="API de la Tienda",
    description="CRUD de productos y categorías organizado con APIRouter",
    version="2.0.0",
    openapi_url="/schema",
)

app.include_router(productos.router)
app.include_router(categorias.router)


@app.get("/", tags=["Inicio"], summary="Mostrar bienvenida")
def inicio():
    return {"mensaje": "API de la Tienda funcionando. Visita /docs"}
