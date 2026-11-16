import os
from flask import Flask, render_template


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "clave-de-desarrollo"),
        DATABASE=os.path.join(app.instance_path, "exploradores.sqlite"),
    )
    if config:
        app.config.update(config)

    os.makedirs(app.instance_path, exist_ok=True)

    from . import db, auth, equipos
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(equipos.bp)

    # Crea la base de datos la primera vez que arranca la app
    with app.app_context():
        if not os.path.exists(app.config["DATABASE"]):
            db.init_db()
        # Solo en producción (Render): crea admin y datos de ejemplo
        if os.environ.get("SEMBRAR_DATOS") == "1":
            from . import semilla
            semilla.sembrar()

    @app.route("/")
    def inicio():
        return render_template("inicio.html")

    return app