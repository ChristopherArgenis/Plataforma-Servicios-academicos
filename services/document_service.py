import docx
from models.document import DocumentModel

class DocumentService:
    """
    Servicio para realizar operaciones de inserción y reemplazo en un documento.
    Opera sobre un objeto DocumentModel.
    """
    def __init__(self, document_model: DocumentModel):
        """
        Inicializa el servicio con un objeto DocumentModel.

        Args:
            document_model (DocumentModel): Una instancia de DocumentModel.
        """
        self.model = document_model

    def insert_text_in_paragraph(self, paragraph_index, text_to_insert):
        """
        Inserta texto en un párrafo específico por su índice utilizando el modelo.

        Args:
            paragraph_index (int): El índice del párrafo (comenzando desde 0).
            text_to_insert (str): El texto a insertar.
        """
        paragraph = self.model.get_paragraph(paragraph_index)
        if paragraph:
            paragraph.add_run(text_to_insert)
        else:
            print(f"El párrafo con el índice {paragraph_index} no existe o el documento no está cargado.")

    def insert_texts_in_paragraphs(self, start_paragraph_index, texts_list):
        """
        Inserta una lista de textos en párrafos consecutivos a partir de un índice inicial
        utilizando el modelo.

        Args:
            start_paragraph_index (int): El índice del primer párrafo a modificar.
            texts_list (list): Una lista de cadenas de texto a insertar en párrafos consecutivos.
        """
        if self.model.is_document_loaded():
            paragraphs = self.model.get_paragraphs()
            for i, text in enumerate(texts_list):
                paragraph_index = start_paragraph_index + i
                if paragraph_index < len(paragraphs):
                    paragraph = paragraphs[paragraph_index]
                    # Limpia lo existente antes de añadir nuevo texto
                    for run in paragraph.runs:
                        run.text = ""
                    paragraph.add_run(text)
                else:
                    print(f"No se pudo insertar '{text}'. El párrafo con el índice {paragraph_index} no existe.")
        else:
            print("No se puede insertar texto. El documento no está cargado.")


    def replace_paragraph_text(self, paragraph_index, new_text):
        """
        Reemplaza el texto completo de un párrafo específico utilizando el modelo.

        Args:
            paragraph_index (int): El índice del párrafo a reemplazar.
            new_text (str): El nuevo texto para el párrafo.
        """
        paragraph = self.model.get_paragraph(paragraph_index)
        if paragraph:
            # Limpiar lo existente
            for run in paragraph.runs:
                run.text = ""
            # Añadir el nuevo texto
            paragraph.add_run(new_text)
        else:
            print(f"El párrafo con el índice {paragraph_index} no existe o el documento no está cargado.")

    def print_document_content(self):
        """
        Imprime el contenido de cada párrafo del documento utilizando el modelo.
        Uso: Comprobacion desde el Script
        """
        if self.model.is_document_loaded():
            print("\n--- Contenido del Documento ---")
            for i, paragraph in enumerate(self.model.get_paragraphs()):
                print(f"Párrafo {i}: {paragraph.text}")
            print("--- Fin del Contenido ---")
        else:
            print("No se puede imprimir el contenido. El documento no está cargado.")

class Plantilla(DocumentService):
    """
    Clase que hereda de DocumentService para realizar reemplazos e inserciones específicas
    en un documento basado en una plantilla.
    """
    def __init__(self, document_model: DocumentModel):
        """
        Inicializa la clase Plantilla con una instancia de DocumentModel y los índices de inicio para inserciones.

        Args:
            document_model (DocumentModel): Una instancia de DocumentModel.
            insertion_start_indices (dict, optional): Un diccionario donde las claves son nombres
                                                     de sección y los valores son los índices de
                                                     párrafo donde comenzar las inserciones.
                                                     Defaults to None.
        """
        super().__init__(document_model)
        self.insertion_start_indices = {"Investigacion":16, "Docencia":27, "Difusion":37,
                                        "Divulgacion":45, "Patentes":47, "Intercambio Académico": 51,
                                        "Proyectos financiados":54, "Participación en comisiones académicas":56,
                                        "Actividades de vinculación":59, "Otros":61,
                                        "3 artículos más importantes/relevantes":65,
                                        "Citas del año":67}

    # Puedes añadir más métodos aquí para operaciones específicas de tu plantilla
    # Por ejemplo, un método para rellenar los datos del investigador
    def complete_researcher_data(self, information: dict):
        """
        Rellena los campos de datos del investigador en la plantilla usando un diccionario.

        Args:
            information (dict): Un diccionario con los datos del investigador (nombre,
                                categoria_nivel, departamento, sni, pride).
        """
        replacements = {
            3: f"Nombre: {information.get('nombre', '')}",
            4: f"Categoría y nivel: {information.get('categoria_nivel', '')}",
            5: f"Departamento: {information.get('departamento', '')}",
            6: f"SNI: {information.get('sni', '')}",
            7: f"PRIDE: {information.get('pride', '')}"
        }
        for index, text in replacements.items():
            self.replace_paragraph_text(index, text)

    # Método para insertar elementos en una sección por nombre o índice
    def insertar_seccion(self, section_key_or_index, items_list):
        """
        Inserta una lista de elementos en una sección específica del documento
        usando una clave de sección (nombre) o un índice de párrafo.

        Args:
            section_key_or_index (str or int): La clave de la sección (nombre, por ejemplo "Investigacion") o
                                               el índice del párrafo donde comenzar a insertar.
            items_list (list): Una lista de cadenas de texto a insertar.

        Example:
            Para insertar en la sección "Investigacion":
            plantilla_instance.insertar_seccion("Investigacion", ["Publicacion 1", "Publicacion 2"])

            Para insertar comenzando en el párrafo con índice 20:
            plantilla_instance.insertar_seccion(20, ["Item 1", "Item 2"])
        """
        start_index = self.insertion_start_indices.get(section_key_or_index, section_key_or_index)
        if isinstance(start_index, int):
            self.insert_texts_in_paragraphs(start_index, items_list)
        else:
            print(f"No se pudo insertar en la sección '{section_key_or_index}'. La clave o índice no es válido.")