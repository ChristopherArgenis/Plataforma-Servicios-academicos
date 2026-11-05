from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
bootstrap = Bootstrap5()

login_manager.login_view = "auth.auth_page"
login_manager.login_message = "Inicia sesión para continuar."
login_manager.login_message_category = "warning"
