import os
from pathlib import Path

import pytest

from podcast_log import create_app
from podcast_log.models import db

BASE_DIR = Path(__file__).parent

os.environ["APP_SETTINGS"] = "podcast_log.config.TestingConfig"


@pytest.fixture(name="app")
def create_test_app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()