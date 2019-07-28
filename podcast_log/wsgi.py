"""WSGI script for launching application via gunicorn."""
from podcast_log import create_app

app = create_app()
