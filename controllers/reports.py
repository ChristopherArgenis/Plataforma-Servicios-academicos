from flask import Blueprint, request, send_file, current_app
from models.document import DocumentModel
from services.document_service import Plantilla
import os

report = Blueprint('reports', __name__)

@report.route('/generate', methods=['POST'])
def generate_report():
    # 1. Load Template
    template_path = os.path.join(current_app.root_path, 'static/templates/Formato_Informe.docx')
    doc_model = DocumentModel(template_path)
    
    if not doc_model.is_document_loaded():
        return "Error loading template", 500

    # 2. Initialize Service
    service = Plantilla(doc_model)

    # 3. Extract Data from Form
    # General Info
    data = {
        'nombre': request.form.get('nombre', ''),
        'categoria_nivel': request.form.get('categoria', ''),
        # Add more fields as needed based on the form
    }
    service.complete_researcher_data(data)

    # Research
    investigacion = request.form.get('investigacion')
    if investigacion:
        service.insertar_seccion("Investigacion", [investigacion])

    libros = request.form.get('libros_cientificos')
    if libros:
        service.insertar_seccion("Investigacion", [f"Libros: {libros}"])

    # Thesis
    titulo_tesis = request.form.get('titulo_tesis')
    if titulo_tesis:
        service.insertar_seccion("Docencia", [f"Tesis: {titulo_tesis}"])

    # Courses
    materia = request.form.get('materia')
    if materia:
        service.insertar_seccion("Docencia", [f"Curso: {materia}"])

    # 4. Save and Download
    # Create temp directory if it doesn't exist
    temp_dir = os.path.join(current_app.root_path, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    output_path = os.path.join(temp_dir, 'reporte_generado.docx')
    doc_model.save(output_path)

    return send_file(output_path, as_attachment=True, download_name="Reporte_Academico.docx")

@report.route('/save_books', methods=['POST'])
def save_books():
    return {'status': 'success', 'message': 'Libros guardados correctamente'}