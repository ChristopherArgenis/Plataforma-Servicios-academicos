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