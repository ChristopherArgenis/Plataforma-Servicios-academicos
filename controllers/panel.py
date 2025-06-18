from flask import Blueprint, render_template, redirect, session, request
# from services.user_service import ArticlesKey_Service
from services.table_manager import TableManager

# Instance of User Service
# Article_Keys = ArticlesKey_Service()
table_maganer = TableManager()

panel_general = Blueprint('panel', __name__)

@panel_general.route('/Panel', methods=["GET", "POST"])
def panel_view():
    profile_id = session['profile_id']
    # Pass profile_id to get_df_table
    dataframe, column_art = table_maganer.get_df_table(profile_id)
    if request.method == "POST":
        title = request.form.get("titulo")
        year = request.form.get('year')
        if title and year:
            try:
                year_int = int(year)
                # Pass profile_id to filter
                dataframe, column_art = table_maganer.filter(profile_id, title, year_int)
            except ValueError:
                flash("Formato de año inválido. Por favor, ingrese un número.", "warning")
                # Optionally, could return the view without this specific filter applied,
                # or redirect, or just let it fall through to render with existing/default dataframe.
                # For now, just flash and let it render the table as it was before this POST.
            except Exception as e:
                flash(f"Error al aplicar filtro: {str(e)}", "danger")
        elif title:
            # Pass profile_id to filter_title
            dataframe, column_art = table_maganer.filter_title(profile_id, title)
        elif year:
            try:
                year_int = int(year)
                # Pass profile_id to filter_year
                dataframe, column_art = table_maganer.filter_year(profile_id, year_int)
            except ValueError:
                flash("Formato de año inválido. Por favor, ingrese un número.", "warning")
            except Exception as e:
                flash(f"Error al aplicar filtro por año: {str(e)}", "danger")

    return render_template('panel.html', df=dataframe, user=session['user_id'], id_articles=column_art.values, years=dataframe.dropna(subset=['year'])["year"].unique().tolist())

@panel_general.route('/Panel/adquirir', methods=["POST"])
def get_articles():
    art_seleccionados = request.form.getlist('keys[]')
    # Add any logic for art_seleccionados if needed in the future
    return redirect(url_for('panel.panel_view'))