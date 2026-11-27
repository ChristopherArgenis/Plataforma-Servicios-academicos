# Plataforma-Servicios-Académicos

Aplicación web diseñada para facilitar la generación de reportes.

## Descripción

Este proyecto proporciona una aplicación web orientada a centralizar, organizar y optimizar los reportes anuales en un entorno web accesible.  
A medida que se desarrolla, se integrarán funcionalidades como gestión de usuarios, adquisición de artículos, generación de reportes y más.

## Instalación

Sigue los siguientes pasos para instalar y ejecutar el proyecto localmente:

## 1. Clona este repositorio

```bash
git clone https://github.com/ChristopherArgenis/Plataforma-Servicios-academicos.git
cd Plataforma-Servicios-academicos
```
# 2. Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```

# 3. Configura las claves privadas (archivo `.env`)
Copia `.env.example` como `.env` y llena los valores. Este archivo **no** se sube a GitHub.
```bash
cp .env.example .env        # En Windows: copy .env.example .env
```
- `SECRET_KEY`: genera una con `python -c "import secrets; print(secrets.token_hex(32))"`
- `SERPAPI_KEY`: clave de SerpAPI de respaldo (opcional, ver abajo)

### Clave de SerpAPI de la institución
El **Super Admin** (rol 3) captura la clave de SerpAPI de la institución en
**Panel > Configuración**. Las consultas a Google Scholar gastan búsquedas de esa cuenta.
- La clave se prueba con SerpAPI antes de guardarse (sin gastar búsquedas) y se guarda cifrada.
- Si no hay clave en Configuración, se usa la de `SERPAPI_KEY` del `.env`, y la página lo avisa.
- Si cambias la `SECRET_KEY`, la clave guardada ya no se puede leer: vuelve a capturarla.

La base de datos `data.db` tampoco se sube al repositorio: se queda solo en tu equipo o servidor.

# 4. Iniciar la aplicación ejecutando el archivo principal del proyecto.
```
python app.py
```

El modo de depuración está apagado por defecto. Para activarlo solo en tu computadora: `FLASK_DEBUG=1 python app.py`.

# Pruebas
```bash
pytest
```
Usan una base de datos temporal: no tocan tu `data.db`.
