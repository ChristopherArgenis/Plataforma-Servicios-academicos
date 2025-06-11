from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from services.user_service import UserService
# from models.QM import Query_Manager
from services.query_maganer import Query_Manager
from models import db

# Instance of User Service
user_service = UserService()

reg_log = Blueprint('user', __name__)

@reg_log.route('/', methods=["GET"])
def auth_page():
    return render_template('auth1.html')

# Route for handling Register
@reg_log.route('/register', methods=['POST'])
def register():
    # Retrieve username and password from the form
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    check = UserService.check_user(username, email)

    if check:
        # If it fails, add failure flash message and redirect to auth page
        flash("Registro Fallido: Ya se capturaron estos datos.", "warning")
        return redirect(url_for('user.auth_page'))
    else:
        # Instance of Query Manager
        query_Manager = Query_Manager(username)
        list_user = query_Manager.get_profile_data()
        dataframe_Articles = query_Manager.get_dataframe()
        
        # Try to register the user using the provided username and password
        user = user_service.register(username, email, password, list_user[0], list_user[1], list_user[2])

        # Try to register the rows of Articles's Table.
        dataframe_Articles.sort_values(by=['year'], ascending=False, inplace=True)
        df_A = dataframe_Articles.to_sql('Articles', con=db.engine, if_exists='append', index=False)

        # If successful, add successful flash message and redirect to auth page
        if user and df_A:
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
    user = user_service.login(email, password)
    # # If successful, add user.id to session and redirect to the list page
    if user:
        session['user_id'] = user.username
        session['profile_id'] = user.profile_id
        return redirect(url_for('panel.panel_view'))
    # If it fails, add failure flash message and redirect to auth page
    else:
        flash("Error: Verificar correo y contraseña", "danger")
        return redirect(url_for('user.auth_page'))
    
# Route for handling logout
@reg_log.route('/logout', methods=['POST'])
def logout():
    # Remove 'user_id' from session to log out the user
    session.pop('user_id', None)
    # Redirect the user to the authentication page after logging out
    return redirect(url_for('user.auth_page'))