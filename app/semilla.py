import os
from werkzeug.security import generate_password_hash
from .db import get_db

EQUIPOS = [
    (
        "Opportunity", "Mars Exploration Rover", "Marte", 2004,
        "Sin contacto desde 2018; misión declarada concluida en 2019",
        "Llegué a Marte en 2004 para una misión de solo 90 días, pero seguí "
        "explorando durante casi 15 años. Una tormenta de polvo cubrió mis "
        "paneles solares en 2018 y nunca volví a comunicarme.",
        "Encontró evidencias de que la zona de Meridiani Planum tuvo agua "
        "líquida en el pasado.",
        None,
    ),
    (
        "Spirit", "Mars Exploration Rover", "Marte", 2004,
        "Atascado en la arena desde 2009; última comunicación en 2010",
        "Aterricé en el cráter Gusev, gemelo de Opportunity. Mis ruedas "
        "quedaron atrapadas en arena blanda, pero desde ahí seguí "
        "estudiando el suelo marciano hasta quedarme sin energía.",
        "Halló depósitos ricos en sílice que sugieren antiguas condiciones "
        "con agua caliente.",
        None,
    ),
    (
        "Surveyor 3", "Programa Surveyor", "Luna", 1967,
        "Inactivo en la Luna; algunas piezas fueron traídas a la Tierra",
        "Aterricé en la Luna en 1967 para probar si el suelo aguantaría a "
        "los astronautas. Años después, la tripulación del Apolo 12 aterrizó "
        "cerca de mí y se llevó algunas de mis piezas para estudiarlas.",
        "Analizó el suelo lunar y ayudó a confirmar que era firme para un "
        "alunizaje tripulado.",
        None,
    ),
    (
        "Etapa de descenso del Eagle", "Apolo 11", "Luna", 1969,
        "Permanece en el Mar de la Tranquilidad",
        "Llevé a Neil Armstrong y Buzz Aldrin hasta la superficie lunar. "
        "Cuando terminó su visita, me quedé en la Luna y sirví de base "
        "para el despegue de la etapa de ascenso.",
        "Junto a ella quedó un retrorreflector láser que todavía se usa "
        "para medir la distancia entre la Tierra y la Luna.",
        None,
    ),
]


def sembrar():
    db = get_db()

    email = os.environ.get("ADMIN_EMAIL", "").strip().lower()
    password = os.environ.get("ADMIN_PASSWORD", "").strip()
    if email and password:
        clave = generate_password_hash(password)
        existe = db.execute(
            "SELECT id FROM usuarios WHERE email = ?", (email,)
        ).fetchone()
        if existe:
            db.execute(
                "UPDATE usuarios SET password_hash = ?, rol = 'admin' "
                "WHERE email = ?", (clave, email))
        else:
            db.execute(
                "INSERT INTO usuarios (nombre, email, password_hash, rol) "
                "VALUES (?, ?, ?, 'admin')",
                ("Administrador", email, clave))
        print(f"[semilla] Administrador listo: {email}", flush=True)
    else:
        print("[semilla] Faltan ADMIN_EMAIL o ADMIN_PASSWORD.", flush=True)

    if db.execute("SELECT COUNT(*) FROM equipos").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO equipos (nombre, mision, ubicacion, anio, estado, "
            "historia, descubrimientos, fuente_url) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            EQUIPOS,
        )

    db.commit()