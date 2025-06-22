from flask import Blueprint, render_template, redirect, url_for, session, request
# from services.user_service import ArticlesKey_Service
from services.table_maganer import Table_Maganer

# Instance of User Service
# Article_Keys = ArticlesKey_Service()
table_maganer = Table_Maganer()

panel_general = Blueprint('panel', __name__)

@panel_general.route('/Panel', methods=["GET"])
def panel_get():
    profile_id = session['scholarKey']
    dataframe, column_art = table_maganer.get_df_table(profile_id)
    return render_template(
        'panel.html',
        df=dataframe,
        user=session['username'],
        id_articles=column_art.values,
        years=dataframe.dropna(subset=['year'])["year"].unique().tolist()
    )

@panel_general.route('/Panel', methods=["POST"])
def panel_post():
    profile_id = session['scholarKey']
    title = request.form.get("titulo")
    year = request.form.get('year')
    
    dataframe, column_art = table_maganer.get_df_table(profile_id)  # Datos base

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

    return render_template(
        'panel.html',
        df=dataframe,
        user=session['username'],
        id_articles=column_art.values,
        years=dataframe.dropna(subset=['year'])["year"].unique().tolist()
    )

@panel_general.route('/Panel/adquirir', methods=["POST"])
def get_articles():
    art_seleccionados = request.form.getlist('keys[]')
    return redirect(url_for('panel.panel_get'))