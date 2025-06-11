from models.user import User, Articles_Keys, db

class UserService:
    @staticmethod
    def register(username, email, password, profile_id, affiliations, cited_by):
        # Create and setup a new User object with the provided username
        new_user = User(username=username, email=email)
        # Hashes the password and stores it securely in the user object
        new_user.set_password(password)
        # Registering the user's Google Scholar information
        new_user.user_info_register(profile_id, affiliations, cited_by)
        # Add the new user object to the database session for saving
        db.session.add(new_user)
        # Commit the transaction to save the new user to the database
        db.session.commit()
        # Return the new user object indicating successful registration
        return new_user
    
    # Login method
    @staticmethod
    def login(email, password):
        # Retrieve user instance using its username
        email = User.query.filter_by(email=email).first()
        # Use the check_password method to compare the passwords
        if email and email.check_password(password):
            # Return the user object if login is successful
            return email
        # Return None if login fails due to invalid credentials
        return None
    
    @staticmethod
    def check_user(username, email):
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user or existing_email:
            return True
        return None
    
class ArticlesKey_Service:
    @staticmethod
    def get_all():
        # Query all Todo entries from the database
        return Articles_Keys.query.all()