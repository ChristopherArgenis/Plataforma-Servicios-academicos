from models.user import User, Articles_Keys, db

class UserService:
    @staticmethod
    def register(username, email, password, profile_id, affiliations, cited_by):
        # Check if a user with the given username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user or existing_email:
            # If user exists, return None indicating registration failure
            return None
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
    def login(username, email, password):
        # Retrieve user instance using its username
        user = User.query.filter_by(username=username).first()
        email = User.query.filter_by(email=email).first()
        # Use the check_password method to compare the passwords
        if user and user.check_password(password) and email:
            # Return the user object if login is successful
            return user
        # Return None if login fails due to invalid credentials
        return None

class UserArticles:
    @staticmethod
    def Store(title, id_Articles, year):
      new_articles = Articles_Keys(title=title, id_Articles=id_Articles, year=year)
      db.session.add(new_articles)
      db.session.commit()
      return new_articles 