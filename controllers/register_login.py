from flask import Blueprint, render_template, request, session, redirect, url_for
from services.user_service import UserService
from models.QM import Query_Manager

# Instance of User Service
user_service = UserService()

reg_log = Blueprint('user', __name__)

@reg_log.route('/', methods=["GET"])
def auth_page():
    return render_template('auth.html')

# Route for handling Register
@reg_log.route('/register', methods=['POST'])
def register():
    # Retrieve username and password from the form
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Instance of Query Manager
    if username:
        query_Manager = Query_Manager(username)

    # Try to register the user using the provided username and password
    user = user_service.register(username, email, password)
    # If successful, add successful flash message and redirect to auth page
    if user:
        return redirect(url_for('user.auth_page'))
    # If it fails, add failure flash message and redirect to auth page
    else:
        return redirect(url_for('user.auth_page'))

# Route for handling login
@reg_log.route('/login', methods=['POST'])
def login():
    # Retrieve username and password from the registration form
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    # Try to login the user using the provided username and password
    user = user_service.login(username, email, password)
    # # If successful, add user.id to session and redirect to the list page
    if user:
        session['user'] = user.username
        return redirect(url_for('panel.panel_view'))
    # If it fails, add failure flash message and redirect to auth page
    else:
        return redirect(url_for('user.auth_page'))
    
# Route for handling logout
@reg_log.route('/logout', methods=['POST'])
def logout():
    # Remove 'user_id' from session to log out the user
    session.pop('user_id', None)
    # Redirect the user to the authentication page after logging out
    return redirect(url_for('user.auth_page'))