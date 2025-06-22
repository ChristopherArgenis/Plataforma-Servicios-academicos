from models.user import Cliente, Usuario, Articles_Keys, db

class LobbyService:
    @staticmethod
    def register(nombre, email, password):
        # Create and setup a new User object with the provided username
        new_customer = Cliente(nombre=nombre, email=email)
        # Hashes the password and stores it securely in the user object
        new_customer.set_password(password)
        # Add the new user object to the database session for saving
        db.session.add(new_customer)
        # Commit the transaction to save the new user to the database
        db.session.commit()
        # Return the new user object indicating successful registration
        return new_customer
    
    # Login method
    @staticmethod
    def login(email, password):
        # Retrieve user instance using its username
        email = Cliente.query.filter_by(email=email).first()
        # Use the check_password method to compare the passwords
        if email and email.check_password(password):
            # Return the user object if login is successful
            return email
        # Return None if login fails due to invalid credentials
        return None
    
    @staticmethod
    def checkCustomer(nombre, email):
        existing_user = Cliente.query.filter_by(nombre=nombre).first()
        existing_email = Cliente.query.filter_by(email=email).first()
        if existing_user or existing_email:
            return True
        return None

class UserService:
    @staticmethod
    def registerUser(id, key):
        # Create and setup a new User object with the provided username
        new_user = Usuario(id=id, profile_id=key)
        # Add the new user object to the database session for saving
        db.session.add(new_user)
        # Commit the transaction to save the new user to the database
        db.session.commit()
        # Return the new user object indicating successful registration
        return new_user
    
    @staticmethod
    def checkUser(id):
        EqualID = Cliente.query.filter_by(id=id).first()
        if EqualID:
            return Usuario.query.filter_by(id=id).first()
        return None

    @staticmethod
    def checkRepeat(key):
        EqualKey = Usuario.query.filter_by(profile_id=key).first()
        if EqualKey:
            return True
        return None
    
class ArticlesKey_Service:
    @staticmethod
    def get_all():
        # Query all Todo entries from the database
        return Articles_Keys.query.all()