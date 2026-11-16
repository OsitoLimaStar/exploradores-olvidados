from app.db import get_db


def test_pagina_registro_carga(client):
    assert client.get("/auth/registro").status_code == 200


def test_registro_crea_usuario_con_contrasena_cifrada(client, auth, app):
    respuesta = auth.registrar()
    assert respuesta.status_code == 302
    assert "/auth/login" in respuesta.headers["Location"]
    with app.app_context():
        usuario = get_db().execute(
            "SELECT * FROM usuarios WHERE email = ?", ("admin@test.com",)
        ).fetchone()
    assert usuario is not None
    assert usuario["password_hash"] != "123456"


def test_primer_usuario_es_admin_y_el_segundo_visitante(client, auth, app):
    auth.registrar()
    auth.registrar("Ana", "ana@test.com")
    with app.app_context():
        filas = get_db().execute(
            "SELECT rol FROM usuarios ORDER BY id").fetchall()
    assert [f["rol"] for f in filas] == ["admin", "visitante"]


def test_registro_rechaza_correo_duplicado(client, auth):
    auth.registrar()
    respuesta = auth.registrar()
    assert respuesta.status_code == 200
    assert "ya está registrado".encode() in respuesta.data


def test_registro_rechaza_contrasena_corta(client, auth):
    respuesta = auth.registrar(password="123")
    assert respuesta.status_code == 200
    assert b"al menos 6 caracteres" in respuesta.data


def test_registro_rechaza_campos_vacios(client, auth):
    respuesta = auth.registrar(nombre="")
    assert respuesta.status_code == 200
    assert b"Completa todos los campos" in respuesta.data


def test_login_correcto_muestra_el_nombre(client, auth):
    auth.registrar()
    respuesta = auth.login()
    assert respuesta.status_code == 302
    assert b"Hola, Admin" in client.get("/").data


def test_login_con_contrasena_incorrecta(client, auth):
    auth.registrar()
    respuesta = auth.login(password="incorrecta")
    assert respuesta.status_code == 200
    assert b"incorrectos" in respuesta.data


def test_logout_cierra_la_sesion(client, auth):
    auth.registrar()
    auth.login()
    auth.logout()
    respuesta = client.get("/equipos/nuevo")
    assert respuesta.status_code == 302
    assert "/auth/login" in respuesta.headers["Location"]