from flask import session, redirect, url_for, request

def require_login_middleware(app):
    # Set up the middleware to run before each request
    @app.before_request
    def require_login():
        # Check if the current endpoint is not in the allowed list
        if request.endpoint not in ['user.auth_page', 'user.register', 'user.login', 'static']:
            # Verify if 'user_id' is in the session; if not, the user is not logged in
            if 'username' not in session:
                # Redirect unauthenticated users to the authentication page
                return redirect(url_for('user.auth_page'))