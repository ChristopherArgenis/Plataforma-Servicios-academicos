# Plataforma-Servicios-Académicos

Aplicación web para generar reportes académicos a partir del perfil de Google Scholar de cada usuario.

## Funciones

- Registro con elección del perfil de Google Scholar e importación automática de artículos (vía SerpAPI).
- Panel con búsqueda por título y año, paginación y estadísticas.
- Selección de artículos («Adquirir») para el reporte.
- Asistente de reporte en 4 pasos: datos, artículos, firma (dibujada o subida) y descarga del PDF.
- Modo demo con datos de ejemplo, sin internet ni costo.

## Inicio rápido

```bash
git clone https://github.com/ChristopherArgenis/Plataforma-Servicios-academicos.git
cd Plataforma-Servicios-academicos
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env            # Windows: copy .env.example .env  (y llena SECRET_KEY y SERPAPI_KEY)
flask --app app init-db
flask --app app seed-demo       # opcional: datos de ejemplo (demo@ejemplo.com / demo1234)
python app.py                   # http://127.0.0.1:3000
```

👉 **Instalación en servidor, configuración y uso detallado: [INSTRUCCIONES.md](INSTRUCCIONES.md)**

## Tecnologías

Flask · Flask-SQLAlchemy · ReportLab (PDF) · Pillow · Flask-Login · Flask-WTF (CSRF) · Bootstrap 5 · SQLite (o MySQL/PostgreSQL) · waitress
