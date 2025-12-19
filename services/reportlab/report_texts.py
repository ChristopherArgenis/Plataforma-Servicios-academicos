# services/reportlab/report_texts.py
# TODO: Cambiar el año
from datetime import datetime

REPORT_TEXTS = {
    "header": f"INFORME ANUAL {datetime.now().year}\n INVESTIGADORES",
    
    "Investigacion": """1. Investigación

Sólo artículos publicados en el año que se evalúa. En todos los casos, dar la referencia completa (título, autores, nombre de la revista, volumen, página, año), DOI, ISSN, factor de impacto y cuartil.

1.1 Publicaciones en revistas con arbitraje
1.2 Publicaciones in extenso en memorias de congresos internacionales
1.3 Publicaciones in extenso en memorias de congresos nacionales
1.4 Libros científicos
1.5 Capítulos de libros científicos""",

    "Docencia": """2. Docencia

2.1 Dirección de tesis y nivel (concluidas y en proceso)
    2.1.1 Doctorado
    2.1.2 Maestría
    2.1.3 Licenciatura

2.2 Cursos impartidos, créditos y nivel (posgrado, licenciatura)

2.3 Participación en comités de tesis y/o tutoriales (nivel, programa de posgrado)

2.4 Participación como jurado en exámenes de grado (nivel, programa de posgrado)

2.5 Estudiantes en proyectos de investigación (posgrado, licenciatura)

2.6 Estudiantes de servicio social durante el período (nombre y procedencia)""",

    "Difusion": """3. Difusión

3.1 Organización de eventos dirigidos a pares (coloquios, conferencias, congresos, cursos, diplomados, foros, mesas redondas, seminarios, simposios, talleres, otros)

3.2 Participación en congresos (título del trabajo, autores, nombre del evento, lugar, fechas, subrayar al ponente, marcar con asterisco a los estudiantes)
    3.2.1 Trabajos presentados en congresos internacionales
    3.2.2 Trabajos presentados en congresos nacionales

3.3 Pláticas invitadas
    3.3.1 Internacionales
    3.3.2 Nacionales

3.4 Participación en otros eventos""",

    "Divulgacion": """4. Divulgación

4.1 Artículos en revistas de divulgación (referencia completa)

4.2 Libros y/o capítulos de libros de divulgación

4.3 Organización de eventos dirigidos a públicos diversos (coloquios, conferencias, congresos, cursos, diplomados, foros, mesas redondas, seminarios, simposios, talleres, otros)

4.4 Participación en eventos""",

    "Patentes": """5. Patentes

Patentes solicitadas u otorgadas en el período.""",

    "IntercambioAcademico": """6. Intercambio Académico

6.1 Visitantes recibidos, extranjeros y nacionales (nombre, institución de procedencia y período de la estancia)

6.2 Visitas y/o estancias académicas realizadas en el extranjero o nacionales (nombre de la institución y período de la estancia)""",

    "ProyectosFinanciados": """7. Proyectos Financiados

Título, participantes (académicos y estudiantes), instituciones, fuente de financiamiento y vigencia.

Clasificar como: Básico, Aplicado, Desarrollo Tecnológico, Innovación""",

    "Comisiones": """8. Participación en Comisiones Académicas

Tanto en la UNAM como externas.""",

    "Vinculacion": """9. Actividades de Vinculación

Servicios técnicos y/o proyectos realizados. Convenios de colaboración institucionales.""",

    "Otros": """10. Otros

Distinciones, premios y reconocimientos.""",

    "Logros": """11. Logros Importantes

Logros relevantes a lo largo de la carrera académica.""",

    "ArticulosRelevantes": """12. Tres Artículos Más Importantes / Relevantes"""
}