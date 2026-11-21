"""Funciones de autenticacion, tokens y control de roles de la API."""

from datetime import datetime, timedelta, timezone
import os

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


# En produccion esta clave se debe configurar como variable de entorno.
SECRET_KEY = os.getenv(
    "SECRET_KEY", "clave-super-secreta-de-mas-de-32-caracteres-cambieme"
)
ALGORITMO = "HS256"
MINUTOS_EXPIRACION = 30


def hashear_password(password: str) -> str:
    """Convierte una contrasena en un hash irreversible."""
    hasheado = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hasheado.decode("utf-8")


def verificar_password(plano: str, hasheado: str) -> bool:
    """Comprueba si una contrasena coincide con su hash guardado."""
    return bcrypt.checkpw(plano.encode("utf-8"), hasheado.encode("utf-8"))


usuarios = [
    {
        "username": "admin",
        "nombre": "Administrador",
        "password": hashear_password("admin123"),
        "rol": "admin",
    },
    {
        "username": "ana",
        "nombre": "Ana Cliente",
        "password": hashear_password("ana123"),
        "rol": "cliente",
    },
]


def buscar_usuario(username: str) -> dict | None:
    """Busca un usuario por su nombre de usuario."""
    for usuario in usuarios:
        if usuario["username"] == username:
            return usuario
    return None


def crear_token(username: str) -> str:
    """Crea un JWT que caduca despues de 30 minutos."""
    expira = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    return jwt.encode(
        {"sub": username, "exp": expira}, SECRET_KEY, algorithm=ALGORITMO
    )


# Hace que Swagger muestre Authorize y lea el token Bearer.
oauth2_esquema = OAuth2PasswordBearer(tokenUrl="/auth/login")


def obtener_usuario_actual(token: str = Depends(oauth2_esquema)) -> dict:
    """Valida el JWT y devuelve el usuario autenticado; si falla responde 401."""
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalido o vencido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        datos = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])
        username = datos.get("sub")
        if username is None:
            raise error
    except jwt.PyJWTError:
        raise error

    usuario = buscar_usuario(username)
    if usuario is None:
        raise error
    return usuario


def requerir_admin(usuario: dict = Depends(obtener_usuario_actual)) -> dict:
    """Permite continuar solo a usuarios con rol administrador; si no, 403."""
    if usuario["rol"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requiere rol de administrador",
        )
    return usuario
