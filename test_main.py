from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def obtener_token(username: str, password: str) -> str:
    respuesta = client.post(
        "/auth/login", data={"username": username, "password": password}
    )
    assert respuesta.status_code == 200
    return respuesta.json()["access_token"]


def encabezado_autorizacion(username: str, password: str) -> dict:
    return {"Authorization": f"Bearer {obtener_token(username, password)}"}


def test_inicio():
    assert client.get("/").status_code == 200


def test_productos_iniciales_y_busqueda():
    respuesta = client.get("/productos")
    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 4
    busqueda = client.get("/productos/buscar", params={"nombre": "AUDÍFONOS"})
    assert busqueda.status_code == 200
    assert busqueda.json()[0]["id"] == 4


def test_crud_producto():
    creado = client.post(
        "/productos",
        json={"nombre": "Webcam HD", "categoria": "Periféricos", "precio": 150000, "disponible": True},
        headers=encabezado_autorizacion("ana", "ana123"),
    )
    assert creado.status_code == 201
    assert creado.json()["creado_por"] == "ana"
    producto_id = creado.json()["producto"]["id"]
    assert client.get(f"/productos/{producto_id}").status_code == 200
    actualizado = client.put(
        f"/productos/{producto_id}",
        json={"nombre": "Webcam Full HD", "categoria": "Periféricos", "precio": 175000, "disponible": True},
        headers=encabezado_autorizacion("ana", "ana123"),
    )
    assert actualizado.status_code == 200
    assert (
        client.delete(
            f"/productos/{producto_id}",
            headers=encabezado_autorizacion("admin", "admin123"),
        ).status_code
        == 200
    )
    assert client.get(f"/productos/{producto_id}").status_code == 404


def test_crud_categoria():
    creada = client.post(
        "/categorias",
        json={"nombre": "Computadores"},
        headers=encabezado_autorizacion("ana", "ana123"),
    )
    assert creada.status_code == 201
    categoria_id = creada.json()["categoria"]["id"]
    assert client.get(f"/categorias/{categoria_id}").status_code == 200
    actualizada = client.put(
        f"/categorias/{categoria_id}",
        json={"nombre": "Portátiles"},
        headers=encabezado_autorizacion("ana", "ana123"),
    )
    assert actualizada.status_code == 200
    assert (
        client.delete(
            f"/categorias/{categoria_id}",
            headers=encabezado_autorizacion("admin", "admin123"),
        ).status_code
        == 200
    )
    assert client.get(f"/categorias/{categoria_id}").status_code == 404


def test_errores_404_y_422():
    assert client.get("/productos/999").status_code == 404
    assert (
        client.post(
            "/productos",
            json={"nombre": "X", "precio": -1},
            headers=encabezado_autorizacion("ana", "ana123"),
        ).status_code
        == 422
    )


def test_seguridad_y_roles():
    # Sin token no se puede crear: 401.
    assert client.post("/productos", json={"nombre": "Tablet", "categoria": "Computadores", "precio": 900000}).status_code == 401

    # Un cliente puede crear, pero no borrar: 403.
    creado = client.post(
        "/categorias",
        json={"nombre": "Seguridad"},
        headers=encabezado_autorizacion("ana", "ana123"),
    )
    assert creado.status_code == 201
    categoria_id = creado.json()["categoria"]["id"]
    assert (
        client.delete(
            f"/categorias/{categoria_id}",
            headers=encabezado_autorizacion("ana", "ana123"),
        ).status_code
        == 403
    )

    # El administrador si puede borrar.
    assert (
        client.delete(
            f"/categorias/{categoria_id}",
            headers=encabezado_autorizacion("admin", "admin123"),
        ).status_code
        == 200
    )


def test_registro_login_y_yo():
    registro = client.post(
        "/auth/registro",
        json={"username": "carlos", "nombre": "Carlos Cliente", "password": "carlos123"},
    )
    assert registro.status_code == 201
    assert registro.json()["usuario"]["rol"] == "cliente"
    assert client.post("/auth/login", data={"username": "carlos", "password": "incorrecta"}).status_code == 401
    respuesta = client.get("/auth/yo", headers=encabezado_autorizacion("carlos", "carlos123"))
    assert respuesta.status_code == 200
    assert respuesta.json()["username"] == "carlos"
