"""Comandos de administración:  flask --app app <comando>"""
import click

from extensions import db
from models import Article, User
from services.scholar import DemoScholar
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
            click.echo(f"  creado: {email} / {password} ({user.articles.count()} artículos)")
        click.echo("Datos de ejemplo cargados.")
