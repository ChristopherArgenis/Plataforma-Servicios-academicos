from models import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    """
    Modelo que representa un usuario de Google Scholar.

    Attributes:
        id (int): Identificador único del usuario.
        profile_id (str): Identificador del perfil del autor.
        affilition (str): Afiliación institucional del autor.
        cited_by (int): Número de citas del autor.
    """
    __tablename__ = 'Usuario'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.String(50), nullable=False)
    affilition = db.Column(db.String(150), nullable=True)
    cited_by = db.Column(db.Integer, nullable=False, default=0)


class Cliente(db.Model):
    """
    Modelo que representa un cliente registrado en el sistema.

    Attributes:
        id (int): Identificador único del cliente.
        rol (int): Rol asignado al cliente (por defecto 0).
        nombre (str): Nombre del cliente.
        email (str): Correo electrónico del cliente.
        password_hash (str): Contraseña encriptada del cliente.
    """
    __tablename__ = 'Cliente'

    id = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.Integer, default=0)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password: str):
        """
        Genera y almacena el hash de la contraseña.

        Args:
            password (str): Contraseña en texto plano.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.

        Args:
            password (str): Contraseña en texto plano.

        Returns:
            bool: True si la contraseña es correcta, False en caso contrario.
        """
        return check_password_hash(self.password_hash, password)


class Articles_Keys(db.Model):
    """
    Modelo que almacena claves de artículos vinculadas a un perfil.

    Attributes:
        id (int): Identificador único.
        title (str): Título del artículo.
        id_Articles (str): Identificador único del artículo.
        year (int): Año de publicación.
        profile_id (str): Identificador del perfil asociado.
    """
    __tablename__ = 'Articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=False, nullable=False)
    id_Articles = db.Column(db.String(100), unique=False, nullable=False)
    year = db.Column(db.Integer, nullable=True, default=0)
    profile_id = db.Column(db.String(150), nullable=False)


class Articles(db.Model):
    """
    Modelo que almacena la información completa de un artículo.

    Attributes:
        id (int): Identificador único.
        id_Articles (str): Identificador del artículo.
        title (str): Título del artículo.
        authors (str): Autores del artículo.
        journal (str): Revista donde fue publicado.
        volume (int): Volumen de la revista.
        pages (str): Páginas del artículo.
        year (int): Año de publicación.
    """
    __tablename__ = 'Article'

    id = db.Column(db.Integer, primary_key=True)
    id_Articles = db.Column(db.String(100), unique=False, nullable=False)
    title = db.Column(db.String(150), unique=False, nullable=False)
    authors = db.Column(db.String(500), unique=False, nullable=True)
    journal = db.Column(db.String(100), unique=False, nullable=True)
    volume = db.Column(db.Integer, unique=False, nullable=True)
    pages = db.Column(db.String(20), unique=False, nullable=False)
    year = db.Column(db.Integer, nullable=True, default=0)


class InformationAcademic(db.Model):
    """
    Modelo que almacena la información académica del usuario para el informe anual.

    Attributes:
        id (int): Identificador único.
        cliente_id (int): ID del cliente asociado.
        sni (str): Nivel SNI.
        pride (str): Nivel PRIDE.
        departamento (str): Departamento de adscripción.
        categoria (str): Categoría y Nivel (ej. "Asociado A").
    """
    __tablename__ = 'InformationAcademic'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)
    sni = db.Column(db.String(50), nullable=True)
    pride = db.Column(db.String(50), nullable=True)
    departamento = db.Column(db.String(100), nullable=True)
    categoria = db.Column(db.String(50), nullable=True)

    cliente = db.relationship('Cliente', backref=db.backref('information_academic', uselist=False))