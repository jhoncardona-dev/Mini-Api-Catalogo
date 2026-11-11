from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


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
    creado = client.post("/productos", json={"nombre": "Webcam HD", "categoria": "Periféricos", "precio": 150000, "disponible": True})
    assert creado.status_code == 201
    producto_id = creado.json()["producto"]["id"]
    assert client.get(f"/productos/{producto_id}").status_code == 200
    actualizado = client.put(f"/productos/{producto_id}", json={"nombre": "Webcam Full HD", "categoria": "Periféricos", "precio": 175000, "disponible": True})
    assert actualizado.status_code == 200
    assert client.delete(f"/productos/{producto_id}").status_code == 200
    assert client.get(f"/productos/{producto_id}").status_code == 404


def test_crud_categoria():
    creada = client.post("/categorias", json={"nombre": "Computadores"})
    assert creada.status_code == 201
    categoria_id = creada.json()["categoria"]["id"]
    assert client.get(f"/categorias/{categoria_id}").status_code == 200
    actualizada = client.put(f"/categorias/{categoria_id}", json={"nombre": "Portátiles"})
    assert actualizada.status_code == 200
    assert client.delete(f"/categorias/{categoria_id}").status_code == 200
    assert client.get(f"/categorias/{categoria_id}").status_code == 404


def test_errores_404_y_422():
    assert client.get("/productos/999").status_code == 404
    assert client.post("/productos", json={"nombre": "X", "precio": -1}).status_code == 422
