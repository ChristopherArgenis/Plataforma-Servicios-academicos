from models.user import User, Article, db

class UserService:
    @staticmethod
    def register(username, email, password, profile_id, affiliations, cited_by, articles_df):
        # Create and setup a new User object with the provided username
        new_user = User(username=username, email=email)
        # Hashes the password and stores it securely in the user object
        new_user.set_password(password)
        # Registering the user's Google Scholar information
        new_user.user_info_register(profile_id, affiliations, cited_by)
        # Add the new user object to the database session for saving
        db.session.add(new_user)
        # It's generally better to commit once after all related objects are added.
        # So, we'll commit after adding articles.

        for index, row in articles_df.iterrows():
            new_article = Article(
                title=row['title'],
                id_Articles=row['id_Articles'], # Make sure this column name matches the DataFrame
                year=row.get('year'), # Use .get() for potentially missing columns like 'year'
                profile_id=profile_id # Associate with the user being registered
            )
            db.session.add(new_article)

        # Commit the transaction to save the new user and their articles
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback() # Rollback in case of error
            # Optionally, re-raise the exception or handle it
            raise e
            # For now, just returning None or False might be too silent.
            # Depending on how the controller handles it, re-raising might be better.

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
    
# ArticlesKey_Service class and its methods are removed as per the plan.