import logging
import os

from flask import Flask, render_template

from config import Config
from extensions import bootstrap, csrf, db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if app.config.get("TRUST_PROXY"):
        # Detrás de Nginx/Apache/IIS: respeta la IP del cliente y si la petición fue HTTPS
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    bootstrap.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from controllers.auth import auth
    from controllers.panel import panel
    from middlewares.request_timing_logger import request_timing_logger

    app.register_blueprint(auth)
    app.register_blueprint(panel)
    request_timing_logger(app)

    @app.errorhandler(404)
    def not_found(_):
        return render_template("error.html", code=404, message="La página no existe."), 404

    @app.errorhandler(413)
    def too_large(_):
        return render_template("error.html", code=413,
                               message="El archivo es demasiado grande (máximo 2 MB)."), 413

    @app.errorhandler(500)
    def server_error(_):
        db.session.rollback()
        return render_template("error.html", code=500, message="Ocurrió un error inesperado."), 500

    from commands import register_commands
    register_commands(app)

    with app.app_context():
        db.create_all()  # crea las tablas que falten (no modifica las existentes)

    return app
