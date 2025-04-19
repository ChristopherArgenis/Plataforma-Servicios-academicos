from flask import Blueprint, render_template, session
# from services.user_service import ArticlesKey_Service
import pandas as pd
from models import db

# Instance of User Service
# Article_Keys = ArticlesKey_Service()

panel_general = Blueprint('panel', __name__)

@panel_general.route('/Panel', methods=["GET"])
def panel_view():
    profile_id = session['profile_id']
    dataframe = pd.read_sql(f'SELECT title, year FROM Articles WHERE profile_id == "{profile_id}"', db.engine)
    dataframe['year'] = pd.to_numeric(dataframe['year'], errors='coerce').astype('Int64')
    return render_template('panel.html', df=dataframe)