from app.db import get_db

DATOS = {
    "nombre": "Rover de prueba",
    "mision": "Misión de prueba",
    "ubicacion": "Marte",
    "anio": "2000",
    "estado": "Inactivo",
    "historia": "Historia de prueba.",
    "descubrimientos": "Descubrimiento de prueba.",
    "fuente_url": "https://science.nasa.gov",
}


def crear(client, **cambios):
    return client.post("/equipos/nuevo", data={**DATOS, **cambios})


def contar_equipos(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM equipos").fetchone()[0]


def test_lista_de_equipos_es_publica(client):
    assert client.get("/equipos/").status_code == 200


def test_anonimo_es_redirigido_al_login(client):
    respuesta = client.get("/equipos/nuevo")
    assert respuesta.status_code == 302
    assert "/auth/login" in respuesta.headers["Location"]


def test_visitante_recibe_403_al_crear(client, auth):
    auth.registrar()                              # admin
    auth.registrar("Ana", "ana@test.com")         # visitante
    auth.login("ana@test.com")
    assert client.get("/equipos/nuevo").status_code == 403
    assert crear(client).status_code == 403


def test_admin_crea_equipo(admin, app):
    respuesta = crear(admin)
    assert respuesta.status_code == 302
    assert contar_equipos(app) == 1
    assert b"Rover de prueba" in admin.get("/equipos/").data


def test_no_crea_con_ubicacion_invalida(admin, app):
    respuesta = crear(admin, ubicacion="Venus")
    assert respuesta.status_code == 200
    assert "Elige una ubicación válida".encode() in respuesta.data
    assert contar_equipos(app) == 0


def test_no_crea_con_campos_obligatorios_vacios(admin, app):
    respuesta = crear(admin, nombre="")
    assert respuesta.status_code == 200
    assert b"Completa nombre" in respuesta.data
    assert contar_equipos(app) == 0


def test_admin_edita_equipo(admin):
    crear(admin)
    respuesta = admin.post("/equipos/1/editar",
                           data={**DATOS, "nombre": "Nombre editado"})
    assert respuesta.status_code == 302
    assert b"Nombre editado" in admin.get("/equipos/1").data


def test_admin_elimina_equipo(admin, app):
    crear(admin)
    respuesta = admin.post("/equipos/1/eliminar")
    assert respuesta.status_code == 302
    assert contar_equipos(app) == 0


def test_visitante_no_puede_eliminar(admin, auth, app):
    crear(admin)
    auth.logout()
    auth.registrar("Ana", "ana@test.com")
    auth.login("ana@test.com")
    assert admin.post("/equipos/1/eliminar").status_code == 403
    assert contar_equipos(app) == 1


def test_busqueda_por_nombre(admin):
    crear(admin, nombre="Rover Alfa")
    crear(admin, nombre="Sonda Beta")
    pagina = admin.get("/equipos/?q=Alfa").data
    assert b"Rover Alfa" in pagina
    assert b"Sonda Beta" not in pagina


def test_filtro_por_ubicacion(admin):
    crear(admin, nombre="Equipo en Marte", ubicacion="Marte")
    crear(admin, nombre="Equipo en la Luna", ubicacion="Luna")
    pagina = admin.get("/equipos/?ubicacion=Luna").data
    assert b"Equipo en la Luna" in pagina
    assert b"Equipo en Marte" not in pagina


def test_detalle_de_equipo_inexistente_da_404(client):
    assert client.get("/equipos/999").status_code == 404