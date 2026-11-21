from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

import seguridad


router = APIRouter(prefix="/productos", tags=["Productos"])


class ProductoEntrada(BaseModel):
    nombre: str = Field(min_length=2)
    categoria: str = Field(min_length=2)
    precio: float = Field(gt=0)
    disponible: bool = True


productos = [
    {"id": 1, "nombre": "Teclado mecánico", "categoria": "Periféricos", "precio": 250000, "disponible": True},
    {"id": 2, "nombre": "Mouse gamer", "categoria": "Periféricos", "precio": 120000, "disponible": True},
    {"id": 3, "nombre": "Monitor de 24 pulgadas", "categoria": "Monitores", "precio": 680000, "disponible": False},
    {"id": 4, "nombre": "Audífonos Asus", "categoria": "Audio", "precio": 80000, "disponible": True},
]


@router.get("", summary="Listar productos")
def listar_productos():
    return productos


@router.get("/buscar", summary="Buscar productos por nombre")
def buscar_productos(nombre: str = Query(min_length=1)):
    texto = nombre.casefold()
    return [producto for producto in productos if texto in producto["nombre"].casefold()]


@router.get("/{producto_id}", summary="Buscar producto por ID")
def obtener_producto(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@router.post("", status_code=status.HTTP_201_CREATED, summary="Crear producto")
def crear_producto(
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    nuevo_id = max((producto["id"] for producto in productos), default=0) + 1
    nuevo = {"id": nuevo_id, **datos.model_dump()}
    productos.append(nuevo)
    return {
        "mensaje": "Producto creado",
        "producto": nuevo,
        "creado_por": usuario["username"],
    }


@router.put("/{producto_id}", summary="Actualizar producto")
def actualizar_producto(
    producto_id: int,
    datos: ProductoEntrada,
    usuario: dict = Depends(seguridad.obtener_usuario_actual),
):
    for producto in productos:
        if producto["id"] == producto_id:
            producto.update(datos.model_dump())
            return {
                "mensaje": "Producto actualizado",
                "producto": producto,
                "actualizado_por": usuario["username"],
            }
    raise HTTPException(status_code=404, detail="Producto no encontrado")


@router.delete("/{producto_id}", summary="Eliminar producto")
def eliminar_producto(
    producto_id: int, admin: dict = Depends(seguridad.requerir_admin)
):
    for producto in productos:
        if producto["id"] == producto_id:
            productos.remove(producto)
            return {
                "mensaje": "Producto eliminado",
                "producto": producto,
                "eliminado_por": admin["username"],
            }
    raise HTTPException(status_code=404, detail="Producto no encontrado")
