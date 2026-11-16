from flask import (Blueprint, abort, flash, redirect,
                   render_template, request, url_for)
from .auth import admin_required
from .db import get_db

bp = Blueprint("equipos", __name__, url_prefix="/equipos")

UBICACIONES = ["Luna", "Marte", "Espacio profundo"]
CAMPOS = ("nombre", "mision", "ubicacion", "anio", "estado",
          "historia", "descubrimientos", "fuente_url")


def obtener_equipo(id):
    equipo = get_db().execute(
        "SELECT * FROM equipos WHERE id = ?", (id,)
    ).fetchone()
    if equipo is None:
        abort(404)
    return equipo


def leer_formulario():
    datos = {c: request.form.get(c, "").strip() for c in CAMPOS}
    error = None
    if not (datos["nombre"] and datos["mision"]
            and datos["estado"] and datos["historia"]):
        error = "Completa nombre, misión, estado e historia."
    elif datos["ubicacion"] not in UBICACIONES:
        error = "Elige una ubicación válida."
    elif datos["anio"] and not datos["anio"].isdigit():
        error = "El año debe ser un número."
    return datos, error


def valores(datos):
    return (
        datos["nombre"], datos["mision"], datos["ubicacion"],
        int(datos["anio"]) if datos["anio"] else None,
        datos["estado"], datos["historia"],
        datos["descubrimientos"] or None, datos["fuente_url"] or None,
    )


# READ: lista con búsqueda y filtro
@bp.route("/")
def lista():
    q = request.args.get("q", "").strip()
    ubicacion = request.args.get("ubicacion", "").strip()

    sql = "SELECT * FROM equipos WHERE 1=1"
    params = []
    if q:
        sql += " AND (nombre LIKE ? OR mision LIKE ?)"
        params += [f"%{q}%", f"%{q}%"]
    if ubicacion in UBICACIONES:
        sql += " AND ubicacion = ?"
        params.append(ubicacion)
    sql += " ORDER BY nombre"

    equipos = get_db().execute(sql, params).fetchall()
    return render_template("equipos/lista.html", equipos=equipos, q=q,
                           ubicacion=ubicacion, ubicaciones=UBICACIONES)


# READ: detalle
@bp.route("/<int:id>")
def detalle(id):
    return render_template("equipos/detalle.html", equipo=obtener_equipo(id))


# CREATE
@bp.route("/nuevo", methods=("GET", "POST"))
@admin_required
def nuevo():
    datos = {}
    if request.method == "POST":
        datos, error = leer_formulario()
        if error:
            flash(error, "error")
        else:
            db = get_db()
            db.execute(
                "INSERT INTO equipos (nombre, mision, ubicacion, anio, estado, "
                "historia, descubrimientos, fuente_url) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", valores(datos))
            db.commit()
            flash("Equipo creado correctamente.", "ok")
            return redirect(url_for("equipos.lista"))
    return render_template("equipos/formulario.html", d=datos,
                           ubicaciones=UBICACIONES, titulo="Nuevo equipo")


# UPDATE
@bp.route("/<int:id>/editar", methods=("GET", "POST"))
@admin_required
def editar(id):
    equipo = obtener_equipo(id)
    datos = {k: ("" if v is None else str(v)) for k, v in dict(equipo).items()}
    if request.method == "POST":
        datos, error = leer_formulario()
        if error:
            flash(error, "error")
        else:
            db = get_db()
            db.execute(
                "UPDATE equipos SET nombre=?, mision=?, ubicacion=?, anio=?, "
                "estado=?, historia=?, descubrimientos=?, fuente_url=? "
                "WHERE id=?", valores(datos) + (id,))
            db.commit()
            flash("Equipo actualizado.", "ok")
            return redirect(url_for("equipos.detalle", id=id))
    return render_template("equipos/formulario.html", d=datos,
                           ubicaciones=UBICACIONES, titulo="Editar equipo")


# DELETE
@bp.route("/<int:id>/eliminar", methods=("POST",))
@admin_required
def eliminar(id):
    obtener_equipo(id)
    db = get_db()
    db.execute("DELETE FROM equipos WHERE id = ?", (id,))
    db.commit()
    flash("Equipo eliminado.", "ok")
    return redirect(url_for("equipos.lista"))