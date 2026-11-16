import pytest
from app import create_app


@pytest.fixture
def app(tmp_path):
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "clave-de-pruebas",
        "DATABASE": str(tmp_path / "prueba.sqlite"),
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


class Acciones:
    def __init__(self, client):
        self._client = client

    def registrar(self, nombre="Admin", email="admin@test.com", password="123456"):
        return self._client.post("/auth/registro", data={
            "nombre": nombre, "email": email, "password": password})

    def login(self, email="admin@test.com", password="123456"):
        return self._client.post("/auth/login", data={
            "email": email, "password": password})

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return Acciones(client)


@pytest.fixture
def admin(client, auth):
    """Registra al primer usuario (que queda como admin) e inicia sesión."""
    auth.registrar()
    auth.login()
    return client