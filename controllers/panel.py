from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from services.user_service import Tables_Service
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
        rol=session['CustomerRol'],
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
        rol=session['CustomerRol'],
        id_articles=column_art.values,
        years=dataframe.dropna(subset=['year'])["year"].unique().tolist()
    )

@panel_general.route('/Panel/adquirir', methods=["POST"])
def get_articles():
    art_seleccionados = request.form.getlist('keys[]')
    return redirect(url_for('panel.panel_get'))

@panel_general.route('/Administracion', methods=["GET"])
def admin_read():
    named_table = request.args.get('table')
    session['nameTable'] = named_table
    match named_table:
        case "Cliente":
            customers = Tables_Service.getCustomer()
            return render_template('admin.html', name=named_table, table=customers)
        case "Usuario":
            users = Tables_Service.getUsers()
            return render_template('admin.html', name=named_table, table=users)

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