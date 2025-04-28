from flask import Blueprint, render_template, session, request
# from services.user_service import ArticlesKey_Service
from services.table_maganer import Table_Maganer

# Instance of User Service
# Article_Keys = ArticlesKey_Service()
table_maganer = Table_Maganer()

panel_general = Blueprint('panel', __name__)

@panel_general.route('/Panel', methods=["GET", "POST"])
def panel_view():
    profile_id = session['profile_id']
    dataframe = table_maganer.get_df_table(profile_id)
    if request.method == "POST":
        title = request.form.get("titulo")
        dataframe = table_maganer.filter_title(title)
    return render_template('panel.html', df=dataframe, user=session['user_id'])