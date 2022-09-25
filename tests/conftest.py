"""Global fixtures for tests."""
from __future__ import annotations

from collections.abc import Generator

import pytest
from click.testing import CliRunner
from flask import Flask
from flask.testing import FlaskClient

from podcast_log import create_app
from podcast_log.models import Episode, Podcast, db


@pytest.fixture(scope="session")
def _app() -> Generator[Flask, None, None]:
    """Construct an app with test configuration. Only happens once per-session."""
    from _pytest.monkeypatch import MonkeyPatch

    monkeypatch = MonkeyPatch()
    monkeypatch.setenv("APP_SETTINGS", "podcast_log.config.TestingConfig")
    yield create_app()
    monkeypatch.undo()


@pytest.fixture(autouse=True)
def app(_app: Flask) -> Generator[Flask, None, None]:
    """Create an application with test settings and empty database.

    Database is cleared after each test.

    Yields:
        The application object with application context.

    """
    with _app.app_context():
        db.create_all()
        yield _app
        db.drop_all()


@pytest.fixture()
def app_with_data(app: Flask) -> Generator[Flask, None, None]:
    """Create an application with pre-filled database."""
    podcast = Podcast(title="Test Podcast")
    [Episode(podcast=podcast) for _ in range(3)]
    podcast.save()
    yield app


@pytest.fixture
def client(app_with_data: Flask) -> FlaskClient:
    """Test client for testing HTTP responses."""
    return app_with_data.test_client()


@pytest.fixture
def runner(app: Flask) -> CliRunner:
    """Command-line runner for flask application."""
    return app.test_cli_runner()
