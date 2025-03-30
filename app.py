from flask import Flask
from flask_bootstrap import Bootstrap5
from controllers.register_login import reg_log
from controllers.panel import panel_general
from middlewares.authentication_middleware import require_login_middleware
from middlewares.request_timing_logger import request_timing_logger
from models import db
from config import Config

app = Flask(__name__)
bootstrap = Bootstrap5(app)

# Load the configuration from the Config class
app.config.from_object(Config)

app.secret_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMTI1IiwibmFtZSI6IkNocmlzdG9waGVyIiwiaWF0IjoxNTE2MjM5MDIyfQ.gO-NHsNnr7YWX_WpO6GM4U6ykuDDyhn38F0T_FrYUl8'

# Initialize the database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

request_timing_logger(app)
require_login_middleware(app)

app.register_blueprint(reg_log)
app.register_blueprint(panel_general)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)