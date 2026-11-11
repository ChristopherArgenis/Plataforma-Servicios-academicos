# test_pdf_gen.py
from app import app
from services.reportlab.report_service import ReportService
import os

def test_generation(cliente_id):
    print(f"Iniciando generación de PDF para cliente_id={cliente_id}...")
    filename = f"informe_cliente_{cliente_id}.pdf"
    
    with app.app_context():
        # Verificamos si existe el cliente o simplemente procedemos (ReportService maneja datos vacíos)
        service = ReportService(cliente_id)
        service.generar_reporte(filename)
    
    if os.path.exists(filename):
        print(f"✅ ÉXITO: {filename} generado correctamente.")
    else:
        print(f"❌ ERROR: No se pudo generar el archivo.")

if __name__ == "__main__":
    # Ajusta el cliente_id según los datos en tu data.db
    # Si no sabes cuál usar, el 1 suele ser el de pruebas.
    test_generation(1)