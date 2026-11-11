import docx

class DocumentModel:
    """
    Modelo para manejar el documento docx.
    """
    def __init__(self, document_path):
        """
        Inicializa el modelo leyendo un documento .docx desde la ruta especificada.

        Args:
            document_path (str): La ruta al archivo .docx.
        """
        try:
            self.document = docx.Document(document_path)
            # print(f"Documento '{document_path}' leído exitosamente.")
        except docx.shared.PackageNotFoundError:
            print(f"Error: El archivo '{document_path}' no se encontró.")
            self.document = None
        except Exception as e:
            print(f"Ocurrió un error al leer el documento: {e}")
            self.document = None

    def get_paragraph(self, index):
        """
        Obtiene un párrafo por su índice.

        Args:
            index (int): El índice del párrafo.

        Returns:
            docx.text.paragraph.Paragraph or None: El objeto párrafo si existe, None en caso contrario.
        """
        if self.document is not None and 0 <= index < len(self.document.paragraphs):
            return self.document.paragraphs[index]
        return None

    def get_paragraphs(self):
        """
        Obtiene todos los párrafos del documento.

        Returns:
            list: Una lista de objetos párrafo.
        """
        if self.document is not None:
            return self.document.paragraphs
        return []

    def is_document_loaded(self):
        """
        Verifica si el documento se cargó correctamente.

        Returns:
            bool: True si el documento está cargado, False en caso contrario.
        """
        return self.document is not None

    def save(self, output_path):
        """
        Guarda el documento.

        Args:
            output_path (str): La ruta donde guardar el documento.
        """
        if self.document is not None:
            try:
                self.document.save(output_path)
                # print(f"Documento guardado exitosamente en '{output_path}'.")
            except Exception as e:
                print(f"Ocurrió un error al guardar el documento: {e}")
        else:
            print("No se puede guardar el documento. El documento no está cargado.")