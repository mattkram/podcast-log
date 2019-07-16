from typing import Generator, Any

import pytest
from datetime import timedelta
from flask import Flask

from podcast_log.models import Podcast, Episode, Status


@pytest.fixture()
def podcast(app: Flask) -> Generator[Podcast, None, None]:
    """Create a test podcast with no episodes."""
    podcast = Podcast(title="Podcast title")
    podcast.save()
    yield podcast


@pytest.fixture()
def episode(podcast: Podcast) -> Generator[Episode, None, None]:
    """Create a test episode which whose status is listened-to."""
    episode = Episode(
        podcast=podcast, duration=timedelta(hours=1), status=Status.LISTENED
    )
    episode.save()
    yield episode


class TestPodcast:
    """Tests for the Podcast model."""

    def test_string_repr(self, podcast: Podcast) -> None:
        """The string representation is the title."""
        assert str(podcast) == podcast.title

    def test_podcast_title(self, podcast: Podcast) -> None:
        """The title is set properly."""
        assert podcast.title == "Podcast title"

    @pytest.mark.parametrize(
        "attr_name,value", [("num_listened", 1), ("time_listened", timedelta(hours=1))]
    )
    @pytest.mark.usefixtures("episode")
    def test_podcast_statistics(
        self, podcast: Podcast, attr_name: str, value: Any
    ) -> None:
        assert getattr(podcast.statistics, attr_name, value)
