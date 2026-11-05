from sqlalchemy.exc import IntegrityError

from extensions import db
from models import Article, User


class RegistrationError(Exception):
    pass


def email_taken(email):
    return db.session.query(User.id).filter_by(email=email).first() is not None


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None


def create_user(name, email, password_hash, profile, articles):
    """Crea el usuario y sus artículos en una sola transacción."""
    user = User(
        name=name,
        email=email,
        password_hash=password_hash,
        scholar_id=profile.author_id,
        scholar_name=profile.name,
        affiliations=profile.affiliations,
        cited_by=profile.cited_by,
    )
    db.session.add(user)
    seen = set()
    for data in articles:
        if data["citation_id"] in seen:
            continue
        seen.add(data["citation_id"])
        db.session.add(Article(user=user, **data))
    try:
        db.session.commit()
    except IntegrityError as exc:
        db.session.rollback()
        raise RegistrationError("Ese correo ya está registrado.") from exc
    return user
