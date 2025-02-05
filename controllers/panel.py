from flask import Blueprint, render_template

panel_general = Blueprint('panel', __name__)

@panel_general.route('/Panel', methods=["GET"])
def panel_view():
    return render_template('panel.html')