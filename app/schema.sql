CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    rol TEXT NOT NULL DEFAULT 'visitante'
        CHECK (rol IN ('admin', 'visitante'))
);

CREATE TABLE IF NOT EXISTS equipos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    mision TEXT NOT NULL,
    ubicacion TEXT NOT NULL
        CHECK (ubicacion IN ('Luna', 'Marte', 'Espacio profundo')),
    anio INTEGER,
    estado TEXT NOT NULL,
    historia TEXT NOT NULL,
    descubrimientos TEXT,
    fuente_url TEXT
);

CREATE TABLE IF NOT EXISTS favoritos (
    usuario_id INTEGER NOT NULL
        REFERENCES usuarios(id) ON DELETE CASCADE,
    equipo_id INTEGER NOT NULL
        REFERENCES equipos(id) ON DELETE CASCADE,
    PRIMARY KEY (usuario_id, equipo_id)
);

CREATE TABLE IF NOT EXISTS comentarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL
        REFERENCES usuarios(id) ON DELETE CASCADE,
    equipo_id INTEGER NOT NULL
        REFERENCES equipos(id) ON DELETE CASCADE,
    texto TEXT NOT NULL,
    fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
