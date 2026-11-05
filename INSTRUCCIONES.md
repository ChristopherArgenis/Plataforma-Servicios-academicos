# Instrucciones de uso — Plataforma de Servicios Académicos

Guía para instalar la plataforma en un servidor propio (Windows o Linux) y usarla.

---

## 1. Requisitos

- **Python 3.10 o superior** (probado con 3.13).
- **Git**.
- Una **clave de SerpAPI** para consultar Google Scholar (https://serpapi.com).
  Sin clave se puede usar el *modo demo* (datos inventados).
- Base de datos: no hace falta instalar nada; por defecto se usa **SQLite**
  (un archivo en `instance/plataforma.db`). Opcionalmente, MySQL o PostgreSQL propios.

---

## 2. Instalación

### Linux / macOS
```bash
git clone https://github.com/ChristopherArgenis/Plataforma-Servicios-academicos.git
cd Plataforma-Servicios-academicos
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Windows (PowerShell)
```powershell
git clone https://github.com/ChristopherArgenis/Plataforma-Servicios-academicos.git
cd Plataforma-Servicios-academicos
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

---

## 3. Configuración (archivo `.env`)

Abre `.env` y llena los valores:

| Variable | Qué es | Ejemplo |
|---|---|---|
| `SECRET_KEY` | Clave para firmar las sesiones. **Obligatoria en producción.** | Genérala con `python -c "import secrets; print(secrets.token_hex(32))"` |
| `SERPAPI_KEY` | Clave de SerpAPI. | `abc123...` |
| `SCHOLAR_PROVIDER` | `serpapi` (real) o `demo` (datos de ejemplo, sin internet). | `serpapi` |
| `DATABASE_URL` | Vacío = SQLite local. Para MySQL/PostgreSQL ver la sección 7. | |
| `SESSION_COOKIE_SECURE` | `1` solo si la app se sirve con HTTPS. | `0` |

> ⚠️ **Nunca subas `.env` ni la base de datos al repositorio.** Ya están en `.gitignore`.

---

## 4. Crear la base de datos

```bash
flask --app app init-db
```

### Cargar datos de ejemplo (opcional)
Crea 3 usuarios con artículos inventados, sin gastar créditos de SerpAPI:
```bash
flask --app app seed-demo
```

| Correo | Contraseña |
|---|---|
| demo@ejemplo.com | demo1234 |
| carlos@ejemplo.com | demo1234 |
| laura@ejemplo.com | demo1234 |

---

## 5. Ejecutar

### Para desarrollo / pruebas
```bash
python app.py
```
Abre http://127.0.0.1:3000

### En el servidor (producción)
Se usa **waitress**, que funciona igual en Windows y Linux:
```bash
waitress-serve --host 0.0.0.0 --port 3000 app:app
```
La app queda disponible en `http://IP-DEL-SERVIDOR:3000` para la red interna.

**Recomendado para producción:**
- Poner un proxy inverso (Nginx, Apache o IIS) delante, con HTTPS, y entonces usar `SESSION_COOKIE_SECURE=1`.
- Dejarla como servicio para que arranque sola:
  - **Linux:** un servicio `systemd`. Ejemplo en `/etc/systemd/system/plataforma.service`:
    ```ini
    [Unit]
    Description=Plataforma de Servicios Academicos
    After=network.target

    [Service]
    WorkingDirectory=/opt/Plataforma-Servicios-academicos
    ExecStart=/opt/Plataforma-Servicios-academicos/venv/bin/waitress-serve --host 127.0.0.1 --port 3000 app:app
    Restart=always
    User=www-data

    [Install]
    WantedBy=multi-user.target
    ```
    Después: `sudo systemctl enable --now plataforma`
  - **Windows:** con [NSSM](https://nssm.cc/) o el Programador de tareas, ejecutando el mismo comando `waitress-serve`.
- **Respaldos:** con SQLite basta copiar `instance/plataforma.db` (con la app detenida o en horario sin uso).

---

## 6. Uso de la plataforma

1. **Registro**
   - Pestaña *Registrarse*: nombre, correo y contraseña (mínimo 8 caracteres).
   - Si tu nombre en Google Scholar es distinto, escríbelo en *Nombre en Google Scholar*.
   - Pulsa **Buscar mi perfil**, elige tu perfil de la lista y pulsa **Confirmar e importar artículos**.
     La importación puede tardar unos segundos.
2. **Iniciar sesión** con correo y contraseña.
3. **Adquisición de artículos**
   - Filtra por año y/o por palabras del título; **Limpiar** quita los filtros.
   - Marca las casillas de los artículos que van en el reporte (la casilla del encabezado marca toda la página)
     y pulsa **Adquirir selección**. La selección se guarda por página: lo que desmarques en esa página se quita.
4. **Reporte** — asistente en 4 pasos:
   1. *Datos a capturar*: tus datos de perfil.
   2. *Artículos*: los seleccionados; puedes **Quitar** cualquiera.
   3. *Firma*: pendiente de implementar.
   4. *Descargar reporte*: por ahora muestra un PDF de ejemplo.
5. **Cuenta**: datos de tu usuario y perfil de Scholar.
6. **Cerrar sesión** con el botón amarillo de arriba a la derecha.

---

## 7. Usar MySQL o PostgreSQL (opcional)

1. Crea una base de datos vacía (por ejemplo `plataforma`) y un usuario con permisos.
2. Instala el conector:
   - MySQL / MariaDB: `pip install pymysql`
   - PostgreSQL: `pip install "psycopg[binary]"`
3. En `.env`:
   ```
   DATABASE_URL=mysql+pymysql://usuario:clave@localhost/plataforma
   # o
   DATABASE_URL=postgresql+psycopg://usuario:clave@localhost/plataforma
   ```
4. `flask --app app init-db`

---

## 8. Pruebas automáticas

```bash
pip install -r requirements-dev.txt
pytest
```
Las pruebas usan una base en memoria y el modo demo: no tocan tus datos ni gastan créditos.

---

## 9. Problemas frecuentes

| Síntoma | Causa / solución |
|---|---|
| "Falta configurar SERPAPI_KEY en el servidor." | Pon la clave en `.env` o usa `SCHOLAR_PROVIDER=demo`. |
| "El servicio de Google Scholar devolvió un error." | Clave inválida o sin créditos. Revisa tu cuenta de SerpAPI y el log del servidor. |
| Las sesiones se cierran al reiniciar el servidor | Falta `SECRET_KEY` en `.env`. |
| Error 400 "The CSRF token is missing" | El formulario se abrió hace mucho o desde otra pestaña: recarga la página. |
| No se puede iniciar sesión tras activar HTTPS | Con `SESSION_COOKIE_SECURE=1` la app **debe** abrirse por `https://`. |
| Tenía un `data.db` de una versión anterior | La nueva versión usa otro esquema y otro archivo (`instance/plataforma.db`). Los usuarios deben registrarse de nuevo; el `data.db` viejo se puede borrar. |

---

## 10. Estructura del proyecto

```
app.py                  Punto de entrada (python app.py / waitress-serve app:app)
factory.py              Crea y configura la aplicación
config.py               Configuración leída de .env
extensions.py           Base de datos, login, CSRF, Bootstrap
commands.py             Comandos: init-db, seed-demo
models/user.py          Tablas: users, articles
controllers/auth.py     Registro, login, logout
controllers/panel.py    Panel, filtros, selección de artículos
services/scholar.py     Consulta a Google Scholar (SerpAPI) y modo demo
services/article_service.py  Búsqueda, filtros y estadísticas de artículos
services/user_service.py     Alta y autenticación de usuarios
templates/, static/     Vistas HTML, CSS y JS
tests/                  Pruebas automáticas (pytest)
```
