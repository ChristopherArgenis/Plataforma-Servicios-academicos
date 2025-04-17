from flask import Blueprint, render_template
from services.user_service import ArticlesKey_Service

# Instance of User Service
Article_Keys = ArticlesKey_Service()

panel_general = Blueprint('panel', __name__)

@panel_general.route('/Panel', methods=["GET"])
def panel_view():
    data = Article_Keys.get_all()
    return render_template('panel.html', data=data)