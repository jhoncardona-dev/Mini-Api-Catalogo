# API de la Tienda

Proyecto actualizado hasta la Guía 3 de FastAPI. Implementa el CRUD de productos y categorías con Pydantic, APIRouter, autenticación JWT y autorización por roles.

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
- `seguridad.py`: hashing de contraseñas, creación y validación de JWT, y control de roles.
- `routers/auth.py`: login, registro de usuarios y consulta del usuario autenticado.
- `routers/productos.py`: modelo, datos y CRUD de productos.
- `routers/categorias.py`: modelo, datos y CRUD de categorías.
- `test_main.py`: pruebas automáticas.

## Seguridad de la Guía 3

Los endpoints `GET` son públicos. Para crear o actualizar se necesita un token; para eliminar se necesita el rol `admin`.

Usuarios iniciales:

- `admin` / `admin123`: puede crear, actualizar y eliminar.
- `ana` / `ana123`: puede crear y actualizar, pero no eliminar.

En Swagger (`/docs`), use `POST /auth/login` con los datos de uno de los usuarios. Copie el valor de `access_token`, pulse **Authorize** y pegue solo el token. Después pruebe los endpoints protegidos.

También puede registrar un cliente desde `POST /auth/registro` y luego iniciar sesión con él.

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

### Autenticación

- `POST /auth/login`
- `POST /auth/registro`
- `GET /auth/yo`

## Respuestas importantes

- `200`: consulta, actualización o eliminación correcta.
- `201`: recurso creado correctamente.
- `404`: el ID solicitado no existe.
- `422`: los datos enviados están incompletos o son inválidos.
- `401`: falta el token, el token venció o no es válido.
- `403`: el usuario inició sesión, pero no tiene permiso para eliminar.

## Ejecutar pruebas

```powershell
python -m pytest -q
```
