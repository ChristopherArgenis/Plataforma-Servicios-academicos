from flask import Blueprint, render_template, session
# from services.user_service import ArticlesKey_Service
from services.table_maganer import Table_Maganer

# Instance of User Service
# Article_Keys = ArticlesKey_Service()
table_maganer = Table_Maganer()

panel_general = Blueprint('panel', __name__)

@panel_general.route('/Panel', methods=["GET"])
def panel_view():
    profile_id = session['profile_id']
    dataframe = table_maganer.get_df_table(profile_id)
    return render_template('panel.html', df=dataframe)