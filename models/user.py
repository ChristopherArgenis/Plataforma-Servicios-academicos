from models import db
from werkzeug.security import generate_password_hash, check_password_hash


# ============================================================
#  MODELOS EXISTENTES
# ============================================================

class Usuario(db.Model):
    __tablename__ = 'Usuario'

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.String(50), nullable=False)
    affilition = db.Column(db.String(150), nullable=True)
    cited_by = db.Column(db.Integer, nullable=False, default=0)


class Cliente(db.Model):
    __tablename__ = 'Cliente'

    id = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.Integer, default=0)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Articles_Keys(db.Model):
    __tablename__ = 'Articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    id_Articles = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, default=0)
    profile_id = db.Column(db.String(150), nullable=False)


class Articles(db.Model):
    __tablename__ = 'Article'

    id = db.Column(db.Integer, primary_key=True)
    id_Articles = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    authors = db.Column(db.String(500), nullable=True)
    journal = db.Column(db.String(100), nullable=True)
    volume = db.Column(db.Integer, nullable=True)
    pages = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, default=0)


class Relevantes(db.Model):
    __tablename__ = 'Relevantes'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)
    id_Articles = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    authors = db.Column(db.String(500), nullable=True)
    journal = db.Column(db.String(100), nullable=True)
    volume = db.Column(db.Integer, nullable=True)
    pages = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, default=0)

    cliente = db.relationship('Cliente', backref=db.backref('relevantes', uselist=False))


class InformationAcademic(db.Model):
    __tablename__ = 'InformationAcademic'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)
    sni = db.Column(db.String(50), nullable=True)
    pride = db.Column(db.String(50), nullable=True)
    departamento = db.Column(db.String(100), nullable=True)
    categoria = db.Column(db.String(50), nullable=True)

    cliente = db.relationship('Cliente', backref=db.backref('information_academic', uselist=False))



# ============================================================
#  NUEVAS TABLAS DEL INFORME ANUAL
# ============================================================

# -------------------------
# LIBROS
# -------------------------
class Libro(db.Model):
    __tablename__ = 'Libro'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)

    libros_cientificos = db.Column(db.String(255), nullable=True)
    capitulos_libro = db.Column(db.String(255), nullable=True)

# -------------------------
# ARTICULOS
# -------------------------
class ArticuloInforme(db.Model):
    __tablename__ = 'ArticuloInforme'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)

    titulo = db.Column(db.Text, nullable=False)
    nivel = db.Column(db.Text, nullable=True)
    nombre_estudiante = db.Column(db.Text, nullable=True)
    institucion = db.Column(db.Text, nullable=True)
    estatus = db.Column(db.Text, nullable=True)


# -------------------------
# CURSOS
# -------------------------
class Curso(db.Model):
    __tablename__ = 'Curso'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)

    materia = db.Column(db.Text, nullable=False)
    nivel = db.Column(db.Text, nullable=True)
    periodo = db.Column(db.Text, nullable=True)
    institucion = db.Column(db.Text, nullable=True)
    programas = db.Column(db.Text, nullable=True)


# -------------------------
# COMITÉ Y JURADO
# -------------------------
class ComiteJurado(db.Model):
    __tablename__ = 'ComiteJurado'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)

    nivel_academico = db.Column(db.Text, nullable=True)
    programa_posgrado = db.Column(db.Text, nullable=True)
    participacion = db.Column(db.Text, nullable=True)  # Se mantendrá como 'Comité - Subtipo'
    titulo_tesis = db.Column(db.Text, nullable=True)
    nombre_estudiante = db.Column(db.Text, nullable=True)


# -------------------------
# ESTUDIANTES
# -------------------------
class Estudiante(db.Model):
    __tablename__ = 'Estudiante'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)

    nombre = db.Column(db.Text, nullable=False)
    actividad = db.Column(db.Text, nullable=True)
    procedencia = db.Column(db.Text, nullable=True)
    titulo_proyecto = db.Column(db.Text, nullable=True)


# -------------------------
# CONGRESOS
# -------------------------
class Congreso(db.Model):
    __tablename__ = 'Congreso'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)

    titulo = db.Column(db.Text, nullable=False)
    autores = db.Column(db.Text, nullable=True)
    nombre = db.Column(db.Text, nullable=True)
    lugar = db.Column(db.Text, nullable=True)
    fechas = db.Column(db.Text, nullable=True)  # Texto para formatos distintos
    ponente = db.Column(db.Text, nullable=True)


class CongresoEstudiante(db.Model):
    __tablename__ = 'CongresoEstudiante'

    id = db.Column(db.Integer, primary_key=True)
    congreso_id = db.Column(db.Integer, db.ForeignKey('Congreso.id'), nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('Estudiante.id'), nullable=False)


# -------------------------
# EVENTOS
# -------------------------
class Evento(db.Model):
    __tablename__ = 'Evento'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)

    tipo = db.Column(db.Text, nullable=True)
    nombre = db.Column(db.Text, nullable=True)
    num_ponentes = db.Column(db.Integer, nullable=True)
    num_asistentes = db.Column(db.Integer, nullable=True)


# -------------------------
# DIVULGACIÓN
# -------------------------
class Divulgacion(db.Model):
    __tablename__ = 'Divulgacion'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)

    tipo_actividad = db.Column(db.Text, nullable=True)
    autores = db.Column(db.Text, nullable=True)
    revista = db.Column(db.Text, nullable=True)
    tipo_evento = db.Column(db.Text, nullable=True)
    modalidad = db.Column(db.Text, nullable=True)


# -------------------------
# ESTANCIAS
# -------------------------
class Estancia(db.Model):
    __tablename__ = 'Estancia'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)

    tipo = db.Column(db.Text, nullable=True)
    nombre = db.Column(db.Text, nullable=True)
    origen = db.Column(db.Text, nullable=True)
    institucion = db.Column(db.Text, nullable=True)
    fechas = db.Column(db.Text, nullable=True)


# -------------------------
# FINANCIAMIENTO
# -------------------------
class Financiamiento(db.Model):
    __tablename__ = 'Financiamiento'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)

    titulo = db.Column(db.Text, nullable=False)
    participantes = db.Column(db.Text, nullable=True)
    fuente = db.Column(db.Text, nullable=True)
    clasificado = db.Column(db.Text, nullable=True)
    indole = db.Column(db.Text, nullable=True)


# -------------------------
# CONTENIDO DE TEXTO ABIERTO
# -------------------------

class Patente(db.Model):
    __tablename__ = 'Patente'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=True)


class Comision(db.Model):
    __tablename__ = 'Comision'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=True)


class Vinculacion(db.Model):
    __tablename__ = 'Vinculacion'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=True)


class Distincion(db.Model):
    __tablename__ = 'Distincion'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=True)


class Logro(db.Model):
    __tablename__ = 'Logro'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Cliente.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=True)