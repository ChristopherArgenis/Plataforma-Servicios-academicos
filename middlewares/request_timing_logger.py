import time

from flask import g, request


def request_timing_logger(app):
    """Registra en el log la ruta, método, código y duración de cada petición."""

    @app.before_request
    def start_timer():
        g.start_time = time.perf_counter()

    @app.after_request
    def log_request_info(response):
        start = g.pop("start_time", None)
        if start is not None and request.endpoint != "static":
            app.logger.info(
                "%s %s -> %s (%.1f ms)",
                request.method, request.path, response.status_code,
                (time.perf_counter() - start) * 1000,
            )
        return response
