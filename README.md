# API de la Tienda

Proyecto actualizado para la Guía 2 de FastAPI. Implementa CRUD completo de productos y categorías usando Pydantic y APIRouter.

## Instalar

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Ejecutar

```powershell
python -m uvicorn main:app --reload
```

Abra `http://127.0.0.1:8000/docs`.

## Organización

- `main.py`: crea la aplicación y conecta los routers.
- `routers/productos.py`: modelo, datos y CRUD de productos.
- `routers/categorias.py`: modelo, datos y CRUD de categorías.
- `test_main.py`: pruebas automáticas.

## Endpoints

### Productos

- `GET /productos`
- `GET /productos/buscar?nombre=monitor`
- `GET /productos/{producto_id}`
- `POST /productos`
- `PUT /productos/{producto_id}`
- `DELETE /productos/{producto_id}`

### Categorías

- `GET /categorias`
- `GET /categorias/{categoria_id}`
- `POST /categorias`
- `PUT /categorias/{categoria_id}`
- `DELETE /categorias/{categoria_id}`

## Respuestas importantes

- `200`: consulta, actualización o eliminación correcta.
- `201`: recurso creado correctamente.
- `404`: el ID solicitado no existe.
- `422`: los datos enviados están incompletos o son inválidos.

## Ejecutar pruebas

```powershell
python -m pytest -q
```
