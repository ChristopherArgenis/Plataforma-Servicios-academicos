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
- `SERPAPI_KEY`: tu clave de SerpAPI

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
