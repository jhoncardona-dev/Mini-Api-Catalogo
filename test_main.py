from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_inicio():
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert "Bienvenido" in respuesta.json()["mensaje"]


def test_lista_productos():
    respuesta = client.get("/productos")
    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 3


def test_producto_existente():
    respuesta = client.get("/productos/2")
    assert respuesta.status_code == 200
    assert respuesta.json()["nombre"] == "Mouse gamer"


def test_producto_inexistente():
    respuesta = client.get("/productos/99")
    assert respuesta.status_code == 404


def test_categorias_sin_repetir():
    respuesta = client.get("/categorias")
    assert respuesta.status_code == 200
    assert respuesta.json() == ["Monitores", "Periféricos"]


def test_busqueda_no_distingue_mayusculas():
    respuesta = client.get("/buscar", params={"nombre": "MOUSE"})
    assert respuesta.status_code == 200
    assert [producto["id"] for producto in respuesta.json()] == [2]
