from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from services import article_service

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

