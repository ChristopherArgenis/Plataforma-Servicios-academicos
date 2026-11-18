import os

from flask import Flask, abort, request
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap5
from controllers.register_login import reg_log
from controllers.panel import panel_general
from controllers.reports import report
from controllers.information import information_bp
from middlewares.authentication_middleware import require_login_middleware
from middlewares.request_timing_logger import request_timing_logger
from models import db
from config import Config

app = Flask(__name__)
bootstrap = Bootstrap5(app)

# Load the configuration from the Config class
app.config.from_object(Config)

# Protección CSRF en todos los formularios y peticiones POST (ver static/js/csrf.js)
csrf = CSRFProtect(app)

# Initialize the database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

request_timing_logger(app)
require_login_middleware(app)

# Los informes viejos que hayan quedado en static/reportes/ ya no se sirven por URL:
# ahora se entregan solo a su dueño desde /Panel/Reporte/informe.pdf
@app.before_request
def block_public_reports():
    if request.path.startswith('/static/reportes/'):
        abort(404)


app.register_blueprint(reg_log)
app.register_blueprint(panel_general)
app.register_blueprint(report)
app.register_blueprint(information_bp)

if __name__ == '__main__':
    # El modo debug solo se activa explícitamente (FLASK_DEBUG=1): expone un depurador
    # que permite ejecutar código en el servidor.
    app.run(
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 3000)),
        debug=os.environ.get('FLASK_DEBUG') == '1',
    )