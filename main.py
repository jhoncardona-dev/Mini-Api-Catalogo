from fastapi import FastAPI, HTTPException, Query


app = FastAPI(
    title="Mini-API de Catálogo",
    description="Catálogo de solo lectura para la evidencia GA1-AA3-EV04",
    version="1.0.0",
)


productos = [
    {
        "id": 1,
        "nombre": "Teclado mecánico",
        "categoria": "Periféricos",
        "precio": 250000,
        "disponible": True,
    },
    {
        "id": 2,
        "nombre": "Mouse gamer",
        "categoria": "Periféricos",
        "precio": 120000,
        "disponible": True,
    },
    {
        "id": 3,
        "nombre": "Monitor de 24 pulgadas",
        "categoria": "Monitores",
        "precio": 680000,
        "disponible": False,
    },
]


@app.get("/", summary="Mostrar bienvenida")
def inicio():
    return {"mensaje": "Bienvenido a la Mini-API de Catálogo"}


@app.get("/productos", summary="Listar productos")
def listar_productos():
    return productos


@app.get("/productos/{producto_id}", summary="Buscar producto por ID")
def obtener_producto(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@app.get("/categorias", summary="Listar categorías sin repetir")
def listar_categorias():
    return sorted({producto["categoria"] for producto in productos})


@app.get("/buscar", summary="Buscar productos por nombre")
def buscar_productos(nombre: str = Query(min_length=1)):
    texto = nombre.casefold()
    return [producto for producto in productos if texto in producto["nombre"].casefold()]
