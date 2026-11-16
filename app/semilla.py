import os
from werkzeug.security import generate_password_hash
from .db import get_db

# Orden de cada equipo:
# (nombre, misión, ubicación, año, estado, historia, descubrimientos, fuente)
EQUIPOS = [
    ("Opportunity", "Mars Exploration Rover", "Marte", 2004,
     "Sin contacto desde 2018; misión declarada concluida en 2019",
     "Llegué a Marte en 2004 para una misión de solo 90 días, pero seguí "
     "explorando durante casi 15 años. Una tormenta de polvo cubrió mis "
     "paneles solares en 2018 y nunca volví a comunicarme.",
     "Encontró evidencias de que la zona de Meridiani Planum tuvo agua "
     "líquida en el pasado.",
     "https://science.nasa.gov/mission/mars-exploration-rovers-spirit-and-opportunity/"),
    ("Spirit", "Mars Exploration Rover", "Marte", 2004,
     "Atascado en la arena desde 2009; última comunicación en 2010",
     "Aterricé en el cráter Gusev, gemelo de Opportunity. Mis ruedas "
     "quedaron atrapadas en arena blanda, pero desde ahí seguí "
     "estudiando el suelo marciano hasta quedarme sin energía.",
     "Halló depósitos ricos en sílice que sugieren antiguas condiciones "
     "con agua caliente.",
     "https://science.nasa.gov/mission/mars-exploration-rovers-spirit-and-opportunity/"),
    ("Surveyor 3", "Programa Surveyor", "Luna", 1967,
     "Inactivo en la Luna; algunas piezas fueron traídas a la Tierra",
     "Aterricé en la Luna en 1967 para probar si el suelo aguantaría a "
     "los astronautas. Años después, la tripulación del Apolo 12 aterrizó "
     "cerca de mí y se llevó algunas de mis piezas para estudiarlas.",
     "Analizó el suelo lunar y ayudó a confirmar que era firme para un "
     "alunizaje tripulado.",
     "https://science.nasa.gov/mission/surveyor-3/"),
    ("Etapa de descenso del Eagle", "Apolo 11", "Luna", 1969,
     "Permanece en el Mar de la Tranquilidad",
     "Llevé a Neil Armstrong y Buzz Aldrin hasta la superficie lunar. "
     "Cuando terminó su visita, me quedé en la Luna y sirví de base "
     "para el despegue de la etapa de ascenso.",
     "Junto a ella quedó un retrorreflector láser que todavía se usa "
     "para medir la distancia entre la Tierra y la Luna.",
     "https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1969-059C"),
    ("Sojourner", "Mars Pathfinder", "Marte", 1997,
     "Inactivo; se quedó para siempre junto al módulo Pathfinder",
     "Fui el primer rover en rodar sobre Marte. Me hicieron para trabajar "
     "una semana, pero funcioné casi tres meses explorando rocas y suelo "
     "cerca de mi módulo de aterrizaje.",
     "Analizó rocas marcianas y demostró que un rover pequeño podía "
     "explorar otro planeta.",
     "https://science.nasa.gov/mission/mars-pathfinder/"),
    ("Viking 1", "Programa Viking", "Marte", 1976,
     "Sin comunicación desde 1982; sigue en Chryse Planitia",
     "Aterricé en 1976 y fui de las primeras máquinas de EE. UU. en "
     "funcionar con éxito en Marte. Mandé algunas de las primeras fotos a "
     "color de la superficie y trabajé más de seis años.",
     "Sus experimentos buscaron señales de vida en el suelo marciano y "
     "estudió el clima del planeta.",
     "https://science.nasa.gov/mission/viking-1/"),
    ("Phoenix", "Misión Phoenix", "Marte", 2008,
     "Sin energía desde el invierno marciano de 2008",
     "Aterricé cerca del polo norte de Marte con un brazo para excavar. "
     "Cavé la tierra helada y encontré hielo de agua. Cuando llegó el "
     "invierno, la luz del Sol desapareció y me quedé sin energía.",
     "Confirmó que hay hielo de agua bajo la superficie cerca del polo "
     "norte de Marte.",
     None),
    ("InSight", "Misión InSight", "Marte", 2018,
     "Sin energía desde 2022; el polvo cubrió sus paneles solares",
     "Llegué a Marte en 2018 para escuchar su interior. Mi sismómetro "
     "captó más de mil terremotos marcianos. Con los años el polvo cubrió "
     "mis paneles solares y mi energía se acabó en 2022.",
     "Detectó terremotos de Marte y reveló cómo es el interior del "
     "planeta.",
     "https://science.nasa.gov/mission/insight/"),
    ("Ingenuity", "Mars 2020", "Marte", 2021,
     "Sus aspas se dañaron en 2024; quedó inmóvil en Marte",
     "Soy el primer helicóptero en volar en otro planeta. Debía hacer 5 "
     "vuelos de prueba y terminé haciendo 72. Un daño en mis aspas puso "
     "fin a mis vuelos en 2024.",
     "Demostró que se puede volar en Marte, donde el aire es muy delgado.",
     "https://science.nasa.gov/mission/mars-2020-perseverance/ingenuity-mars-helicopter/"),
    ("Vehículo Lunar (moon buggy)", "Apolo 15, 16 y 17", "Luna", 1971,
     "Los tres están estacionados para siempre en la Luna",
     "Fuimos tres autos eléctricos que ayudaron a los astronautas a "
     "recorrer la Luna. Gracias a nosotros pudieron alejarse de su módulo "
     "y traer rocas de lugares lejanos. Al terminar, nos quedamos "
     "estacionados.",
     "Permitió explorar más lejos y recoger muestras de rocas lunares "
     "para estudiarlas en la Tierra.",
     "https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1971-063C"),
    ("Paquetes científicos ALSEP", "Apolo 12 al 17", "Luna", 1969,
     "Apagados en 1977; siguen en la superficie",
     "Los astronautas nos dejaron en la Luna con sismómetros y otros "
     "instrumentos. Enviamos datos a la Tierra durante años, hasta que en "
     "1977 nos apagaron.",
     "Sus sismómetros detectaron temblores en la Luna, llamados lunamotos.",
     "https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1969-099C"),
    ("Pioneer 10", "Misión Pioneer", "Espacio profundo", 1972,
     "Última señal en 2003; sigue viajando lejos del Sol",
     "Fui la primera nave en cruzar el cinturón de asteroides y en "
     "visitar Júpiter. Sigo viajando hacia las estrellas con una placa que "
     "muestra de dónde vengo.",
     "Tomó los primeros datos de cerca de Júpiter y mostró que se puede "
     "cruzar el cinturón de asteroides.",
     "https://science.nasa.gov/mission/pioneer-10/"),
    ("Telescopio Espacial Kepler", "Misión Kepler", "Espacio profundo", 2009,
     "Sin combustible desde 2018; sigue a la deriva siguiendo a la Tierra",
     "Pasé nueve años observando miles de estrellas para encontrar "
     "planetas fuera de nuestro sistema solar. Cuando se me acabó el "
     "combustible, me apagaron en 2018.",
     "Descubrió miles de exoplanetas y mostró que los planetas son muy "
     "comunes en la galaxia.",
     "https://science.nasa.gov/mission/kepler/"),
    ("Dawn", "Misión Dawn", "Espacio profundo", 2007,
     "Sin combustible desde 2018; orbita sola el planeta enano Ceres",
     "Visité dos mundos del cinturón de asteroides: Vesta y Ceres. Fui la "
     "primera nave en orbitar dos cuerpos distintos del sistema solar. Hoy "
     "sigo girando en silencio alrededor de Ceres.",
     "Mapeó Vesta y Ceres y mostró que Ceres tiene manchas brillantes de "
     "sales.",
     "https://science.nasa.gov/mission/dawn/"),
    ("NEAR Shoemaker", "Misión NEAR", "Espacio profundo", 1996,
     "Descansa sobre el asteroide Eros desde 2001",
     "Orbité el asteroide Eros y, aunque no fui construida para aterrizar, "
     "lo logré en 2001. Fui la primera nave en posarse sobre un asteroide.",
     "Mapeó Eros y mostró cómo es la superficie de un asteroide.",
     "https://science.nasa.gov/mission/near-shoemaker/"),
]


def sembrar():
    db = get_db()

    # Sincroniza el administrador con las variables de entorno
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

    # Carga los equipos de ejemplo solo si la tabla está vacía
    if db.execute("SELECT COUNT(*) FROM equipos").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO equipos (nombre, mision, ubicacion, anio, estado, "
            "historia, descubrimientos, fuente_url) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            EQUIPOS,
        )

    db.commit()