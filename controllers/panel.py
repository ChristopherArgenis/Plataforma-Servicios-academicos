from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from services.user_service import Tables_Service, Check_Article
from services.table_maganer import Table_Maganer
from services.query_maganer import Query_Manager
from services.articles_maganer import Articles_Maganer
from models import db

table_maganer = Table_Maganer()
articles_maganer = Articles_Maganer()
check_article = Check_Article()

panel_general = Blueprint('panel', __name__)

@panel_general.route('/Panel', methods=["GET"])
def panel_get():
    # Default view is Acquisition
    return panel_acquisition()

@panel_general.route('/Panel/Acquisition', methods=["GET"])
def panel_acquisition():
    profile_id = session['scholarKey']
    dataframe, column_art = table_maganer.get_df_table(profile_id)
    select_year = dataframe.dropna(subset=['year'])["year"].unique().tolist()
    
    context = {
        'df': dataframe,
        'user': session['username'],
        'rol': session['CustomerRol'],
        'id_articles': column_art.values,
        'years': select_year,
        'active_page': 'acquisition'
    }

    if request.headers.get('HX-Request'):
        return render_template('partials/acquisition.html', **context)
    
    return render_template('base_panel.html', **context)

@panel_general.route('/Panel/Info', methods=["GET"])
def panel_info():
    context = {
        'user': session['username'],
        'rol': session['CustomerRol'],
        'active_page': 'info'
    }
    
    if request.headers.get('HX-Request'):
        return render_template('partials/info.html', **context)
    
    return render_template('base_panel.html', **context)

@panel_general.route('/Panel/Report', methods=["GET"])
def panel_report():
    context = {
        'user': session['username'],
        'rol': session['CustomerRol'],
        'active_page': 'report'
    }
    
    if request.headers.get('HX-Request'):
        return render_template('partials/report.html', **context)
    
    return render_template('base_panel.html', **context)

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

    context = {
        'df': dataframe,
        'user': session['username'],
        'rol': session['CustomerRol'],
        'id_articles': column_art.values,
        'years': dataframe.dropna(subset=['year'])["year"].unique().tolist(),
        'active_page': 'acquisition'
    }
    
    if request.headers.get('HX-Request'):
         return render_template('partials/acquisition.html', **context)

    return render_template('base_panel.html', **context)

@panel_general.route('/Panel/Update_Table', methods=["POST"])
def table_update():
    table_maganer.delete_articles(session['scholarKey'])
    query_Manager = Query_Manager(session['scholarKey'])
    dataframe_Articles = query_Manager.get_dataframe()
    df_A = dataframe_Articles.to_sql('Articles', con=db.engine, if_exists='append', index=False)
    return redirect(url_for('panel.panel_get'))

@panel_general.route('/Panel/adquirir', methods=["POST"])
def get_articles():
    art_selects = request.form.getlist('keys[]')
    nrA = check_article.repeat_articles(art_selects)
    if len(nrA) > 0:
        dataframe = articles_maganer.df_articles(array=nrA)
        insert_db = dataframe.to_sql('Article', con=db.engine, if_exists='append', index=False)
        flash(f"{len(nrA)} consultados exitosamente.", "success")
    else:
        flash("Todos los Articulos ya estan almacenados", "success")
    return redirect(url_for('panel.panel_get'))

@panel_general.route('/Administracion', methods=["GET"])
def admin_read():
    named_table = request.args.get('table')
    session['nameTable'] = named_table
    rol = session['CustomerRol']
    match named_table:
        case "Cliente":
            customers = Tables_Service.getCustomer()
            return render_template('admin.html', name=named_table, table=customers, rol=rol)
        case "Usuario":
            users = Tables_Service.getUsers()
            return render_template('admin.html', name=named_table, table=users, rol=rol)

@panel_general.route('/Admin/crear', methods=["POST"])
def admin_create():
    table = session['nameTable']
    match table:
        case "Cliente":
            rol = request.form.get('rol')
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            customer = Tables_Service.createCustomer(rol, name, email, password)
            if customer:
                flash("Cliente exitosamente registrado.", "success")
                return redirect(url_for('panel.admin_read', table=table))
            else:
                flash("Error al registrar al cliente.", "danger")
                return redirect(url_for('panel.admin_read', table=table))
        case "Usuario":
            id = request.form.get('create-id')
            profile_id = request.form.get('key')
            cited_by = request.form.get('cites')
            user = Tables_Service.createUser(id, profile_id, cited_by)
            if user == "Success":
                flash("Usuario exitosamente registrado.", "success")
                return redirect(url_for('panel.admin_read', table=table))
            elif user == "Existent":
                flash("Clave Registrada: La clave esta registrada", "warning")
                return redirect(url_for('panel.admin_read', table=table))
            else:
                flash("ID sin asociar: El ID no esta asociado a un cliente", "danger")
                return redirect(url_for('panel.admin_read', table=table))

@panel_general.route('/Admin/actualizar', methods=["POST"])
def admin_update():
    table = session['nameTable']
    match table:
        case "Cliente":
            id = request.form.get('update-id')
            rol = request.form.get('rol')
            updateRol = Tables_Service.updateCustomerRol(id, rol)
            if updateRol:
                flash("Actualizacion de rol exitoso.", "success")
                return redirect(url_for('panel.admin_read', table=table))
            else:
                flash("Actualizacion de rol fallido.", "warning")
                return redirect(url_for('panel.admin_read', table=table))

@panel_general.route('/Admin/eliminar', methods=["POST"])
def admin_delete():
    id = request.form.get('delete-id')
    table = session['nameTable']
    match table:
        case "Cliente":
            customer = Tables_Service.deleteCustomer(id)
            if customer:
                return redirect(url_for('panel.admin_read', table=table))
            else:
                print("No existe el id")
        case "Usuario":
            user = Tables_Service.deleteUser(id)
            if user:
                return redirect(url_for('panel.admin_read', table=table))
            else:
                print("No existe el id")