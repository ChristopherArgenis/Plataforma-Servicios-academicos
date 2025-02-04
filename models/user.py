from models import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    # Define the primary key for the User table
    id = db.Column(db.Integer, primary_key=True)
    # Define a column for username, ensuring it's unique and cannot be null
    username = db.Column(db.String(150), unique=True, nullable=False)
    # Define a column for email, ensuring it's unique and cannot be null
    email = db.Column(db.String(150), unique=True, nullable=False)
    # Define a column to store the hashed password, not storing it as plain text
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        # Convert the plain password to a hashed password for security
        self.password_hash = generate_password_hash(password)

    # Method to compare given password with the hashed one
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)