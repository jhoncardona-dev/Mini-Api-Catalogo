# Mini-API de Catálogo

Evidencia **GA1-AA3-EV04** de la Guía 1 de APIs con FastAPI. La aplicación publica un catálogo de productos almacenado temporalmente en memoria.

## Requisitos

- Python 3.10 o superior
- Visual Studio Code

## Instalación en Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell impide activar el entorno, ejecute una vez en esa terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Ejecutar la API

```powershell
uvicorn main:app --reload
```

Abra:

- API: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

- `GET /`: devuelve un mensaje de bienvenida.
- `GET /productos`: devuelve los tres productos.
- `GET /productos/{producto_id}`: busca por ID y responde 404 si no existe.
- `GET /categorias`: devuelve categorías distintas.
- `GET /buscar?nombre=mouse`: busca coincidencias parciales sin distinguir mayúsculas.

## Pruebas automáticas

```powershell
pytest -q
```

## Evidencia en Swagger UI

En `/docs`, pruebe los cinco endpoints con **Try it out** y **Execute**. Capture la operación y la respuesta. Para el endpoint por ID use `2`; para la búsqueda use `mouse`.

## Publicar en GitHub

```powershell
git init
git add .
git commit -m "Completar Mini-API de Catalogo"
git branch -M main
git remote add origin URL_DE_SU_REPOSITORIO
git push -u origin main
```

Reemplace `URL_DE_SU_REPOSITORIO` por la dirección creada en GitHub. El enlace final depende de su cuenta y por eso no se puede completar de forma automática en esta entrega.
