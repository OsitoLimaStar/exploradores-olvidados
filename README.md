# Exploradores Olvidados

Aplicación web hecha con Flask y SQLite para el NASA Space Apps Challenge 2026.

**Reto:** Abandonados pero no olvidados: narración sobre el equipo descartado de la NASA en la Luna y Marte.

**Solución:** un catálogo de hardware que la NASA dejó en la Luna, Marte y el espacio profundo, con la historia de cada equipo contada para estudiantes de escuela.

**Aplicación desplegada:** https://exploradores-olvidados.onrender.com

## Funciones
- Registro, inicio y cierre de sesión.
- Roles: `admin` (el primer usuario registrado) y `visitante`.
- CRUD de equipos (solo admin), con búsqueda y filtro por ubicación.
- Pruebas automatizadas con pytest.

## Cómo ejecutarlo
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python run.py

## Pruebas
    pytest -v

## Estructura
- `app/`: aplicación (auth, equipos, base de datos, plantillas)
- `tests/`: pruebas automatizadas
- `run.py`: punto de entrada

## Autor
[Jorge A. Colquehuanca Lopez]
[Christian G. Castro Daza]