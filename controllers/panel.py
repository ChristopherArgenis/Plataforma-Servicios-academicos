import io
import re
import unicodedata
from datetime import datetime

from flask import (
    Blueprint, abort, current_app, flash, redirect, render_template, request, send_file, url_for,
)
from flask_login import current_user, login_required

from services import article_service, signature_service
from services.report_pdf import build_report
from services.signature_service import SignatureError

panel = Blueprint("panel", __name__)


def _filters(source):
    """Lee título y año de un formulario o de la URL, ignorando valores inválidos."""
    title = source.get("titulo", "").strip()[:200]
    try:
        year = int(source.get("year", ""))
    except ValueError:
        year = None
    return title, year


def _back_to_panel(title, year, page=None):
    params = {k: v for k, v in {"titulo": title, "year": year, "page": page}.items() if v}
    return redirect(url_for("panel.panel_view", **params))


@panel.route("/panel", methods=["GET"])
@login_required
def panel_view():
    title, year = _filters(request.args)
    page = request.args.get("page", 1, type=int)
    pagination = article_service.search(current_user, title, year).paginate(
        page=page, per_page=current_app.config["ARTICLES_PER_PAGE"], error_out=False
    )
    return render_template(
        "panel.html",
        pagination=pagination,
        title=title,
        year=year,
        years=article_service.years(current_user),
        stats=article_service.stats(current_user),
        selected_articles=article_service.search(current_user, only_selected=True).all(),
        signature=current_user.signature,
        initial_step=min(max(request.args.get("paso", 1, type=int), 1), 4),
    )


@panel.route("/panel/adquirir", methods=["POST"])
@login_required
def acquire():
    """Guarda la selección de la página visible: marcados -> sí, desmarcados -> no."""
    visible = {int(i) for i in request.form.getlist("visible_ids") if i.isdigit()}
    checked = {int(i) for i in request.form.getlist("keys") if i.isdigit()} & visible
    article_service.set_selection(current_user, checked, True)
    article_service.set_selection(current_user, visible - checked, False)
    total = article_service.stats(current_user)["selected"]
    flash(f"Selección guardada. Tienes {total} artículo(s) para el reporte.", "success")
    title, year = _filters(request.form)
    return _back_to_panel(title, year, request.form.get("page", type=int))


@panel.route("/panel/quitar/<int:article_id>", methods=["POST"])
@login_required
def unselect(article_id):
    article_service.set_selection(current_user, [article_id], False)
    return redirect(url_for("panel.panel_view", _anchor="reporte"))



def _to_report_step(step):
    return redirect(url_for("panel.panel_view", paso=step, _anchor="reporte"))


@panel.route("/panel/firma", methods=["POST"])
@login_required
def save_signature():
    signer_name = request.form.get("signer_name", "").strip()[:150]
    signer_title = request.form.get("signer_title", "").strip()[:150]
    if not signer_name:
        flash("Escribe el nombre de quien firma.", "danger")
        return _to_report_step(3)

    upload = request.files.get("signature_file")
    drawn = request.form.get("signature_data", "")
    try:
        raw = None
        if upload and upload.filename:
            raw = upload.read(signature_service.MAX_BYTES + 1)
        elif drawn:
            raw = signature_service.decode_data_url(drawn)
        png = signature_service.normalize(raw) if raw is not None else None
        signature_service.save(current_user, signer_name, signer_title, png)
    except SignatureError as exc:
        flash(str(exc), "danger")
        return _to_report_step(3)
    flash("Firma guardada.", "success")
    return _to_report_step(4)


@panel.route("/panel/firma/borrar", methods=["POST"])
@login_required
def delete_signature():
    signature_service.delete(current_user)
    flash("Firma eliminada.", "info")
    return _to_report_step(3)


@panel.route("/panel/firma.png")
@login_required
def signature_image():
    sig = current_user.signature
    if sig is None:
        abort(404)
    resp = send_file(io.BytesIO(sig.image), mimetype="image/png")
    resp.headers["Cache-Control"] = "private, no-store"
    return resp


def _slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "reporte"


@panel.route("/panel/reporte.pdf")
@login_required
def report_pdf():
    articles = article_service.search(current_user, only_selected=True).all()
    if not articles:
        flash("Selecciona al menos un artículo para generar el reporte.", "warning")
        return _to_report_step(2)
    now = datetime.now()
    pdf = build_report(current_user, articles, current_user.signature, now)
    filename = f"reporte-{_slug(current_user.name)}-{now:%Y-%m-%d}.pdf"
    resp = send_file(
        io.BytesIO(pdf), mimetype="application/pdf",
        as_attachment=request.args.get("descargar") == "1", download_name=filename,
    )
    resp.headers["Cache-Control"] = "private, no-store"
    return resp
