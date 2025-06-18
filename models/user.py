from models import db
from werkzeug.security import generate_password_hash, check_password_hash

# Tabla de asociación user_roles
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('Users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('Roles.id'), primary_key=True)
)

class Role(db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'

class User(db.Model):
    __tablename__ = 'Users'

    # Define the primary key for the User table
    id = db.Column(db.Integer, primary_key=True)
    # Define a column for username, ensuring it's unique and cannot be null
    username = db.Column(db.String(150), unique=True, nullable=False)
    # Define a column for email, ensuring it's unique and cannot be null
    email = db.Column(db.String(150), unique=True, nullable=False)
    # Define a column to store the hashed password, not storing it as plain text
    password_hash = db.Column(db.String(200), nullable=False)
    # Define a column for profile_id, cannot be null
    profile_id = db.Column(db.String(150), nullable=False)
    # Define a column for affiliations, cannot be null
    affiliations = db.Column(db.String(150), nullable=False)
    # Define a column for cited_by, cannot be null
    cited_by = db.Column(db.Integer, nullable=True, default=0)

    # Relación con Role
    roles = db.relationship('Role', secondary=user_roles,
                            backref=db.backref('users', lazy='dynamic'),
                            lazy='dynamic')

    def set_password(self, password):
        # Convert the plain password to a hashed password for security
        self.password_hash = generate_password_hash(password)

    # Method to compare given password with the hashed one
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def user_info_register(self, profile_id, affiliations, cited_by):
        self.profile_id = profile_id
        self.affiliations = affiliations
        self.cited_by = cited_by
    
class Article(db.Model):
    __tablename__ = 'articles'

    # Define the primary key for the User table
    id = db.Column(db.Integer, primary_key=True)
    # Define a column for title, ensuring it's not unique and cannot be null
    title = db.Column(db.String(150), nullable=False)
    # Define a column for id_Articles, ensuring it's unique and cannot be null
    id_Articles = db.Column(db.String(100), nullable=False)
    # Define a column to store the year and cannot be null
    year = db.Column(db.Integer, nullable=True, default=0)
    # Define a column for profile_id, cannot be null
    profile_id = db.Column(db.String(150), nullable=False)

    __table_args__ = (db.UniqueConstraint('id_Articles', 'profile_id', name='uq_article_profile'),)