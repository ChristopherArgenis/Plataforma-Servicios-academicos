from models import db
from models.user import Cliente, InformationAcademic


class InfoService:
    """
    Servicio para manejar la información académica de los usuarios.
    """

    @staticmethod
    def save_informacion_academica(username: str, data: dict) -> tuple[bool, str]:
        """
        Guarda o actualiza la información académica de un usuario.

        Args:
            username (str): Nombre del usuario.
            data (dict): Diccionario con los datos académicos (sni, pride, departamento, categoria).

        Returns:
            tuple[bool, str]: (éxito, mensaje)
        """
        try:
            # Buscar el cliente
            cliente = Cliente.query.filter_by(nombre=username).first()
            
            if not cliente:
                return False, 'Usuario no encontrado.'

            # Verificar si ya existe información académica
            info_academica = InformationAcademic.query.filter_by(cliente_id=cliente.id).first()

            if info_academica:
                # Actualizar registro existente
                info_academica.sni = data.get('sni')
                info_academica.pride = data.get('pride')
                info_academica.departamento = data.get('departamento')
                info_academica.categoria = data.get('categoria')
                mensaje = 'Información actualizada correctamente.'
            else:
                # Crear nuevo registro
                new_info = InformationAcademic(
                    cliente_id=cliente.id,
                    sni=data.get('sni'),
                    pride=data.get('pride'),
                    departamento=data.get('departamento'),
                    categoria=data.get('categoria')
                )
                db.session.add(new_info)
                mensaje = 'Información guardada correctamente.'

            db.session.commit()
            return True, mensaje

        except Exception as e:
            db.session.rollback()
            return False, f'Error al guardar la información: {str(e)}'

    @staticmethod
    def update_nombre_cliente(current_username: str, new_name: str) -> tuple[bool, str]:
        """
        Actualiza el nombre del cliente.
        """
        try:
            cliente = Cliente.query.filter_by(nombre=current_username).first()
            if not cliente:
                return False, 'Usuario no encontrado'
            
            cliente.nombre = new_name
            db.session.commit()
            return True, 'Nombre actualizado correctamente'
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def get_informacion_academica(username: str) -> dict:
        """
        Obtiene la información académica de un usuario.

        Args:
            username (str): Nombre del usuario.

        Returns:
            dict: Diccionario con la información académica o None si no existe.
        """
        try:
            cliente = Cliente.query.filter_by(nombre=username).first()
            
            if not cliente:
                return None

            info_academica = InformationAcademic.query.filter_by(cliente_id=cliente.id).first()

            if not info_academica:
                return None

            return {
                'sni': info_academica.sni,
                'pride': info_academica.pride,
                'departamento': info_academica.departamento,
                'categoria': info_academica.categoria
            }

        except Exception as e:
            print(f"Error al obtener información académica: {e}")
            return None
