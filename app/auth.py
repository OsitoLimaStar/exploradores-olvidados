import functools
from flask import (Blueprint, abort, flash, g, redirect,
                   render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/registro", methods=("GET", "POST"))
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        db = get_db()
        error = None

        if not nombre or not email or not password:
            error = "Completa todos los campos."
        elif len(password) < 6:
            error = "La contraseña debe tener al menos 6 caracteres."
        elif db.execute(
            "SELECT id FROM usuarios WHERE email = ?", (email,)
        ).fetchone():
            error = "Ese correo ya está registrado."

        if error is None:
            # El primer usuario registrado será el administrador
            total = db.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
            rol = "admin" if total == 0 else "visitante"
            db.execute(
                "INSERT INTO usuarios (nombre, email, password_hash, rol) "
                "VALUES (?, ?, ?, ?)",
                (nombre, email, generate_password_hash(password), rol),
            )
            db.commit()
            flash("Registro exitoso. Ahora inicia sesión.", "ok")
            return redirect(url_for("auth.login"))

        flash(error, "error")

    return render_template("auth/registro.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        usuario = get_db().execute(
            "SELECT * FROM usuarios WHERE email = ?", (email,)
        ).fetchone()

        if usuario is None or not check_password_hash(
            usuario["password_hash"], password
        ):
            flash("Correo o contraseña incorrectos.", "error")
        else:
            session.clear()
            session["usuario_id"] = usuario["id"]
            return redirect(url_for("inicio"))

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))


@bp.before_app_request
def cargar_usuario():
    usuario_id = session.get("usuario_id")
    if usuario_id is None:
        g.usuario = None
    else:
        g.usuario = get_db().execute(
            "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped(**kwargs):
        if g.usuario is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped


def admin_required(view):
    @functools.wraps(view)
    def wrapped(**kwargs):
        if g.usuario is None:
            return redirect(url_for("auth.login"))
        if g.usuario["rol"] != "admin":
            abort(403)
        return view(**kwargs)
    return wrapped