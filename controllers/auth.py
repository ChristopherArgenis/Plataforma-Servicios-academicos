import re
from dataclasses import asdict

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash

from services import user_service
from services.scholar import Profile, ScholarError, get_scholar_client

auth = Blueprint("auth", __name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MIN_PASSWORD = 8


@auth.route("/", methods=["GET"])
def auth_page():
    if current_user.is_authenticated:
        return redirect(url_for("panel.panel_view"))
    return render_template("auth.html", tab=request.args.get("tab", "login"))


@auth.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    user = user_service.authenticate(email, password)
    if not user:
        flash("Correo o contraseña incorrectos.", "danger")
        return redirect(url_for("auth.auth_page"))
    session.clear()  # evita reutilizar una sesión anterior
    login_user(user)
    return redirect(url_for("panel.panel_view"))


@auth.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    password2 = request.form.get("password2", "")
    scholar_name = request.form.get("scholar_name", "").strip() or name

    errors = []
    if not name:
        errors.append("Escribe tu nombre.")
    if not EMAIL_RE.match(email):
        errors.append("El correo no es válido.")
    if len(password) < MIN_PASSWORD:
        errors.append(f"La contraseña debe tener al menos {MIN_PASSWORD} caracteres.")
    if password != password2:
        errors.append("Las contraseñas no coinciden.")
    if not errors and user_service.email_taken(email):
        errors.append("Ese correo ya está registrado. Inicia sesión.")
    if errors:
        for e in errors:
            flash(e, "danger")
        return redirect(url_for("auth.auth_page", tab="register"))

    try:
        profiles = get_scholar_client().search_profiles(scholar_name)
    except ScholarError as exc:
        flash(str(exc), "danger")
        return redirect(url_for("auth.auth_page", tab="register"))
    if not profiles:
        flash(f"No se encontraron perfiles de Google Scholar para «{scholar_name}».", "warning")
        return redirect(url_for("auth.auth_page", tab="register"))

    # Se guarda el registro pendiente (con la contraseña ya cifrada) hasta elegir perfil
    session["pending_registration"] = {
        "name": name,
        "email": email,
        "password_hash": generate_password_hash(password),
        "profiles": [asdict(p) for p in profiles[:10]],
    }
    return redirect(url_for("auth.choose_profile"))


@auth.route("/register/perfil", methods=["GET", "POST"])
def choose_profile():
    pending = session.get("pending_registration")
    if not pending:
        return redirect(url_for("auth.auth_page", tab="register"))
    profiles = [Profile(**p) for p in pending["profiles"]]

    if request.method == "GET":
        return render_template("choose_profile.html", profiles=profiles, name=pending["name"])

    profile = next((p for p in profiles if p.author_id == request.form.get("author_id")), None)
    if not profile:
        flash("Selecciona uno de los perfiles de la lista.", "warning")
        return redirect(url_for("auth.choose_profile"))

    try:
        articles = get_scholar_client().get_articles(profile.author_id)
        user = user_service.create_user(
            pending["name"], pending["email"], pending["password_hash"], profile, articles
        )
    except (ScholarError, user_service.RegistrationError) as exc:
        flash(str(exc), "danger")
        return redirect(url_for("auth.auth_page", tab="register"))

    session.clear()
    login_user(user)
    current_app.logger.info("Usuario registrado: %s (%d artículos)", user.email, len(articles))
    flash(f"Registro exitoso. Se importaron {len(articles)} artículos.", "success")
    return redirect(url_for("panel.panel_view"))


@auth.route("/register/cancelar", methods=["POST"])
def cancel_registration():
    session.pop("pending_registration", None)
    return redirect(url_for("auth.auth_page", tab="register"))


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("auth.auth_page"))
