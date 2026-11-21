"""Rutas para iniciar sesion, registrar usuarios y consultar el usuario actual."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

import seguridad


router = APIRouter(prefix="/auth", tags=["Autenticacion"])


class RegistroEntrada(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    nombre: str = Field(min_length=2, max_length=80)
    password: str = Field(min_length=6)


@router.post("/login", summary="Iniciar sesion y obtener token")
def login(datos: OAuth2PasswordRequestForm = Depends()):
    usuario = seguridad.buscar_usuario(datos.username)
    if usuario is None or not seguridad.verificar_password(
        datos.password, usuario["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contrasena incorrectos",
        )

    token = seguridad.crear_token(usuario["username"])
    return {"access_token": token, "token_type": "bearer"}


@router.post(
    "/registro",
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario cliente",
)
def registrar_usuario(datos: RegistroEntrada):
    if seguridad.buscar_usuario(datos.username) is not None:
        raise HTTPException(status_code=409, detail="El usuario ya existe")

    nuevo_usuario = {
        "username": datos.username,
        "nombre": datos.nombre,
        "password": seguridad.hashear_password(datos.password),
        "rol": "cliente",
    }
    seguridad.usuarios.append(nuevo_usuario)
    return {
        "mensaje": "Usuario registrado",
        "usuario": {
            "username": nuevo_usuario["username"],
            "nombre": nuevo_usuario["nombre"],
            "rol": nuevo_usuario["rol"],
        },
    }


@router.get("/yo", summary="Consultar el usuario del token")
def quien_soy(usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    return {
        "username": usuario["username"],
        "nombre": usuario["nombre"],
        "rol": usuario["rol"],
    }
