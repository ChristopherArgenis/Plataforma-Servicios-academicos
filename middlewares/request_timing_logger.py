from flask import request, g
import time

# Function to add timing middleware to our app
def request_timing_logger(app):
    # This function runs before each request
    @app.before_request
    def start_timer():
        # Save the current time when the request starts
        g.start_time = time.time()

    # This function runs after each request
    @app.after_request
    def log_request_info(response):
        # Calculate the duration of the request
        # Si otra verificación cortó la petición antes de iniciar el cronómetro
        # (p. ej. CSRF), no hay hora de inicio: se registra sin duración.
        start = g.get('start_time')
        if start is None:
            return response
        duration = time.time() - start
        # Print the request details and duration to the console
        print("-" * 60)
        print(f"Path: {request.path} | Method: {request.method} | Duration: {duration:.4f} seconds")
        print("-" * 60)
        return response