from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    # Datos del perfil de Google Scholar
    scholar_id = db.Column(db.String(50), nullable=False)
    scholar_name = db.Column(db.String(150), nullable=False)
    affiliations = db.Column(db.String(255), nullable=False, default="")
    cited_by = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    articles = db.relationship(
        "Article", back_populates="user", cascade="all, delete-orphan", lazy="dynamic"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Article(db.Model):
    __tablename__ = "articles"
    __table_args__ = (db.UniqueConstraint("user_id", "citation_id"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    citation_id = db.Column(db.String(100), nullable=False)
    title = db.Column(db.Text, nullable=False)
    authors = db.Column(db.Text, nullable=False, default="")
    publication = db.Column(db.Text, nullable=False, default="")
    year = db.Column(db.Integer, nullable=True, index=True)
    cited_by = db.Column(db.Integer, nullable=False, default=0)
    link = db.Column(db.Text, nullable=False, default="")
    # Marcado por el usuario con "Adquirir" para incluirlo en el reporte
    selected = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship("User", back_populates="articles")
