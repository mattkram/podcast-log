from typing import Any, Generator

import pytest
from click.testing import CliRunner
from flask import Flask
from flask.testing import FlaskClient

from podcast_log import create_app
from podcast_log.models import db, Podcast, Episode


@pytest.fixture(name="app")
def create_test_app(monkeypatch: Any) -> Generator[Flask, None, None]:
    monkeypatch.setenv("APP_SETTINGS", "podcast_log.config.TestingConfig")
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture()
def app_with_data(app: Flask) -> Generator[Flask, None, None]:
    podcast = Podcast(title="Test Podcast")
    [Episode(podcast=podcast) for _ in range(3)]
    podcast.save()
    yield app


@pytest.fixture
def client(app_with_data: Flask) -> FlaskClient:
    return app_with_data.test_client()


@pytest.fixture
def runner(app: Flask) -> CliRunner:
    return app.test_cli_runner()
