import os
from flask import Flask


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "clave-de-desarrollo"),
        DATABASE=os.path.join(app.instance_path, "exploradores.sqlite"),
    )
    if config:
        app.config.update(config)

    os.makedirs(app.instance_path, exist_ok=True)

    from . import db
    db.init_app(app)

    # Crea la base de datos la primera vez que arranca la app
    with app.app_context():
        if not os.path.exists(app.config["DATABASE"]):
            db.init_db()

    @app.route("/")
    def inicio():
        return "Exploradores Olvidados: funciona!"

    return app
