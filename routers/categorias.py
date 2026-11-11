from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field


router = APIRouter(prefix="/categorias", tags=["Categorías"])


class CategoriaEntrada(BaseModel):
    nombre: str = Field(min_length=2)


categorias = [
    {"id": 1, "nombre": "Periféricos"},
    {"id": 2, "nombre": "Monitores"},
    {"id": 3, "nombre": "Audio"},
]


@router.get("", summary="Listar categorías")
def listar_categorias():
    return categorias


@router.get("/{categoria_id}", summary="Buscar categoría por ID")
def obtener_categoria(categoria_id: int):
    for categoria in categorias:
        if categoria["id"] == categoria_id:
            return categoria
    raise HTTPException(status_code=404, detail="Categoría no encontrada")


@router.post("", status_code=status.HTTP_201_CREATED, summary="Crear categoría")
def crear_categoria(datos: CategoriaEntrada):
    nuevo_id = max((categoria["id"] for categoria in categorias), default=0) + 1
    nueva = {"id": nuevo_id, "nombre": datos.nombre}
    categorias.append(nueva)
    return {"mensaje": "Categoría creada", "categoria": nueva}


@router.put("/{categoria_id}", summary="Actualizar categoría")
def actualizar_categoria(categoria_id: int, datos: CategoriaEntrada):
    for categoria in categorias:
        if categoria["id"] == categoria_id:
            categoria["nombre"] = datos.nombre
            return {"mensaje": "Categoría actualizada", "categoria": categoria}
    raise HTTPException(status_code=404, detail="Categoría no encontrada")


@router.delete("/{categoria_id}", summary="Eliminar categoría")
def eliminar_categoria(categoria_id: int):
    for categoria in categorias:
        if categoria["id"] == categoria_id:
            categorias.remove(categoria)
            return {"mensaje": "Categoría eliminada", "categoria": categoria}
    raise HTTPException(status_code=404, detail="Categoría no encontrada")
