from sqlalchemy import case, func

from extensions import db
from models import Article


def _escape_like(text):
    return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def search(user, title="", year=None, only_selected=False):
    """Consulta (sin ejecutar) de artículos del usuario con filtros opcionales."""
    query = Article.query.filter_by(user_id=user.id)
    if title:
        query = query.filter(Article.title.ilike(f"%{_escape_like(title)}%", escape="\\"))
    if year is not None:
        query = query.filter(Article.year == year)
    if only_selected:
        query = query.filter(Article.selected.is_(True))
    # Sin año al final (portable: SQLite, MySQL y PostgreSQL)
    return query.order_by(Article.year.is_(None), Article.year.desc(), Article.title)


def years(user):
    rows = (
        db.session.query(Article.year)
        .filter(Article.user_id == user.id, Article.year.isnot(None))
        .distinct()
        .order_by(Article.year.desc())
    )
    return [r[0] for r in rows]


def set_selection(user, article_ids, selected):
    """Marca o desmarca artículos; solo afecta a los del propio usuario."""
    if not article_ids:
        return 0
    count = (
        Article.query.filter(Article.user_id == user.id, Article.id.in_(article_ids))
        .update({Article.selected: selected}, synchronize_session=False)
    )
    db.session.commit()
    return count


def stats(user):
    total, citations, selected = db.session.query(
        func.count(Article.id),
        func.coalesce(func.sum(Article.cited_by), 0),
        func.coalesce(func.sum(case((Article.selected.is_(True), 1), else_=0)), 0),
    ).filter(Article.user_id == user.id).one()
    return {"total": total, "citations": citations, "selected": selected}
