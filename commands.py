"""Comandos de administración:  flask --app app <comando>"""
import io
import math

import click
from PIL import Image, ImageDraw

from extensions import db
from models import Article, User
from services.scholar import DemoScholar
from services import signature_service
from services.user_service import create_user
from werkzeug.security import generate_password_hash

DEMO_USERS = [
    ("Dra. Ana López Ruiz", "demo@ejemplo.com", "demo1234"),
    ("Dr. Carlos Méndez Soto", "carlos@ejemplo.com", "demo1234"),
    ("Mtra. Laura Gutiérrez Peña", "laura@ejemplo.com", "demo1234"),
]


def register_commands(app):
    @app.cli.command("init-db")
    def init_db():
        """Crea las tablas de la base de datos."""
        db.create_all()
        click.echo("Base de datos lista.")

    @app.cli.command("seed-demo")
    def seed_demo():
        """Carga usuarios y artículos de ejemplo (no usa SerpAPI)."""
        scholar = DemoScholar()
        for name, email, password in DEMO_USERS:
            if User.query.filter_by(email=email).first():
                click.echo(f"  ya existe: {email}")
                continue
            profile = scholar.search_profiles(name)[0]
            user = create_user(name, email, generate_password_hash(password),
                               profile, scholar.get_articles(profile.author_id))
            # Algunos artículos recientes ya seleccionados para el reporte
            recent = user.articles.filter(Article.year >= 2023).limit(5).all()
            for art in recent:
                art.selected = True
            db.session.commit()
            if email == DEMO_USERS[0][1]:
                signature_service.save(user, name, "Profesora investigadora", _demo_signature())
            click.echo(f"  creado: {email} / {password} ({user.articles.count()} artículos)")
        click.echo("Datos de ejemplo cargados.")


def _demo_signature():
    """Firma inventada (trazo ondulado) para el usuario de ejemplo."""
    img = Image.new("RGBA", (700, 220), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    pts = [(40 + x, 120 + 45 * math.sin(x / 38) * math.exp(-x / 900) - x / 12)
           for x in range(0, 560, 4)]
    draw.line(pts, fill=(11, 31, 58, 255), width=6, joint="curve")
    draw.line([(90, 165), (610, 140)], fill=(11, 31, 58, 255), width=4)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return signature_service.normalize(buf.getvalue())
