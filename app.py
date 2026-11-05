"""Punto de entrada.

Desarrollo:   python app.py
Producción:   waitress-serve --host 0.0.0.0 --port 3000 app:app
"""
import os

from factory import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", 3000)),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
