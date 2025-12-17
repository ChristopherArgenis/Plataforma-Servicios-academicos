from models.user import Cliente, Usuario, Articles_Keys, Articles, Relevantes, db

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
    def registerUser(id, key, affilition, cited_by):
        # Create and setup a new User object with the provided username
        new_user = Usuario(id=id, profile_id=key, affilition=affilition, cited_by=cited_by)
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

class Tables_Service:
    # Seccion "Create" - Crear
    @staticmethod
    def createCustomer(rol, name, email, password):
        new_customer = Cliente(rol=rol, nombre=name, email=email)
        new_customer.set_password(password)
        db.session.add(new_customer)
        db.session.commit()
        return new_customer
    
    @staticmethod
    def createUser(id, profile_id, cited_by):
        EqualID = Cliente.query.filter_by(id=id).first()
        EqualKey = Usuario.query.filter_by(profile_id=profile_id).first()
        if EqualKey:
            return "Existent"
        elif EqualID:
            new_user = Usuario(id=id, profile_id=profile_id, cited_by=cited_by)
            db.session.add(new_user)
            db.session.commit()
            return "Success"
        else:
            return None
    
    # Seccion "Update" - Actualizar
    @staticmethod
    def updateCustomerRol(id, rol):
        customer = Cliente.query.get(id)
        customer.rol = rol
        db.session.commit()
        return customer
    
    # Seccion "Read" - Leer
    @staticmethod
    def getCustomer():
        return Cliente.query.all()
    
    @staticmethod
    def getUsers():
        return Usuario.query.all()
    
    @staticmethod
    def getArticleskeys():
        return Articles_Keys.query.all()

    # Seccion "Delete" - Eliminar
    @staticmethod
    def deleteCustomer(id):
        customer = Cliente.query.get(id)
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return customer
        else:
            return None
        
    @staticmethod
    def deleteUser(id):
        user = Usuario.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return user
        else:
            return None

class Check_Article:
    @staticmethod
    def repeat_articles(send_array):
        article_clean = []
        for key in send_array:
            process_repeat = Articles.query.filter_by(id_Articles=key).first()
            if not process_repeat:
                article_clean.append(key)
        return article_clean
    
    @staticmethod
    def repeat_relevantes(send_array):
        article_clean = []
        for key in send_array:
            process_repeat = Relevantes.query.filter_by(id_Articles=key).first()
            if not process_repeat:
                article_clean.append(key)
        return article_clean