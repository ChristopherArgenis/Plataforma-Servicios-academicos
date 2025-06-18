from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from services.user_service import UserService
# from models.QM import Query_Manager
from services.query_manager import QueryManager
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
        query_manager = QueryManager() # Nueva instanciación

        try:
            list_user = query_manager.get_profile_data(username) # Nueva llamada
        except ValueError as e:
            flash(f"Error al obtener perfil: {str(e)}", "danger")
            return redirect(url_for('user.auth_page'))

        # El author_id es el primer elemento de list_user
        if not list_user or not list_user[0]:
            flash("Error: No se pudo obtener el ID del perfil del autor.", "danger")
            return redirect(url_for('user.auth_page'))

        author_id_for_articles = list_user[0]
        dataframe_articles = query_manager.get_articles_dataframe(author_id_for_articles) # Nueva llamada

        # Try to register the user using the provided username and password
        # Asegurarse que list_user tiene suficientes elementos si se accede por índice directamente
        # Pass the dataframe_articles to the register method
        try:
            user = user_service.register(username, email, password, list_user[0], list_user[1], list_user[2], dataframe_articles)
            if user: # Check if user object is returned (implies success)
                flash("El Registro ha sido Exitoso", "success")
                return redirect(url_for('user.auth_page'))
            else:
                # This case might occur if register returns None explicitly without an exception
                flash("Registro Fallido: No se pudo crear el usuario.", "danger")
                return redirect(url_for('user.auth_page'))
        except Exception as e:
            # Catch exceptions from user_service.register (e.g., database errors during commit)
            flash(f"Error durante el registro: {str(e)}", "danger")
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
    # Remove 'user_id' and 'profile_id' from session to log out the user
    session.pop('user_id', None)
    session.pop('profile_id', None)
    # Redirect the user to the authentication page after logging out
    return redirect(url_for('user.auth_page'))