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
    dataframe, column_art = table_maganer.get_df_table(profile_id)
    if request.method == "POST":
        title = request.form.get("titulo")
        year = request.form.get('year')
        if title and year:
            try:
                year = int(year)
                dataframe, column_art = table_maganer.filter(title, year)
            except:
                pass
        elif title:
            dataframe, column_art = table_maganer.filter_title(title)
        elif year:
            try:
                year = int(year)
                dataframe, column_art = table_maganer.filter_year(year)
            except:
                pass
        else:
            art_seleccionados = request.form.getlist('keys[]')
    return render_template('panel.html', df=dataframe, user=session['user_id'], id_articles=column_art.values, years=dataframe.dropna(subset=['year'])["year"].unique().tolist())