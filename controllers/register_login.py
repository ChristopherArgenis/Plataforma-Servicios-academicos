from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from services.user_service import LobbyService, UserService
# from models.QM import Query_Manager
from services.query_maganer import Query_Manager
from models import db

reg_log = Blueprint('user', __name__)

@reg_log.route('/', methods=["GET"])
def auth_page():
    return render_template('auth1.html')

@reg_log.route('/Key', methods=["GET"])
def key_view():
    return render_template("claveScholar.html")

@reg_log.route('/Access', methods=["POST"])
def access_key():
    # Obtener la Clave
    key = request.form['scholarKey']
    # Checar si clave se repite
    repeat = UserService.checkRepeat(key)
    if key == "":
        flash("Por favor, ingrese su Clave.", "danger")
        return redirect(url_for('user.key_view'))
    elif repeat:
        flash("Esta clave ya esta registrada", "warning")
        return redirect(url_for('user.key_view'))
    else:
        session['scholarKey'] = key
        id = session["userID"]
        query_Manager = Query_Manager(key)
        affilition, cited_by = query_Manager.get_profile_data()
        # Registrar al nuevo usuario
        user = UserService.registerUser(id, key, affilition, cited_by)
        # Si se registro exitosamente
        if user:
            dataframe_Articles = query_Manager.get_dataframe()
            df_A = dataframe_Articles.to_sql('Articles', con=db.engine, if_exists='append', index=False)
            return redirect(url_for('panel.panel_get'))

# Route for handling Register
@reg_log.route('/register', methods=['POST'])
def register():
    # Retrieve username and password from the form
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    check = LobbyService.checkCustomer(username, email)

    if check:
        # If it fails, add failure flash message and redirect to auth page
        flash("Registro Fallido: Ya se capturaron estos datos.", "warning")
        return redirect(url_for('user.auth_page'))
    else:
        # Try to register the user using the provided username and password
        user = LobbyService.register(username, email, password)

        # If successful, add successful flash message and redirect to auth page
        if user:
            flash("El Registro ha sido Exitoso", "success")
            return redirect(url_for('user.auth_page'))
        else:
            flash("Registro Fallido: Error en captura de datos", "danger")
            return redirect(url_for('user.auth_page'))

# Route for handling login
@reg_log.route('/login', methods=['POST'])
def login():
    # Retrieve username and password from the registration form
    email = request.form['email']
    password = request.form['password']
    # Try to login the user using the provided username and password
    customer = LobbyService.login(email, password)
    # # If successful, add user.id to session and redirect to the list page
    if customer and customer.rol != 0:
        session['username'] = customer.nombre
        user = UserService.checkUser(customer.id)
        if user:
            session['scholarKey'] = user.profile_id
            session['CustomerRol'] = customer.rol
            return redirect(url_for('panel.panel_get'))
        else:
            session["userID"] = customer.id
            return redirect(url_for('user.key_view'))
    elif customer and customer.rol == 0:
        flash("Acceso Denegado: No tiene permisos de usuario", "warning")
        return redirect(url_for('user.auth_page'))
    # If it fails, add failure flash message and redirect to auth page
    else:
        flash("Error: Verificar correo y contraseña", "danger")
        return redirect(url_for('user.auth_page'))
    
# Route for handling logout
@reg_log.route('/logout', methods=['POST'])
def logout():
    # Remove 'user_id' from session to log out the user
    session.pop('username', None)
    # Redirect the user to the authentication page after logging out
    return redirect(url_for('user.auth_page'))