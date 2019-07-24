"""WSGI script for launching application via gunicorn."""
from podcast_log import create_app

if __name__ == "__main__":
    app = create_app()
