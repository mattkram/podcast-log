from typing import Generator, Any

import pytest
from datetime import timedelta, datetime
from flask import Flask

from podcast_log.models import Podcast, Episode, Status


@pytest.fixture()
def podcast(app: Flask) -> Generator[Podcast, None, None]:
    """Create a test podcast with no episodes."""
    podcast = Podcast(title="Podcast title", image_url="http://podcast-image-url.com")
    podcast.save()
    yield podcast


@pytest.fixture()
def episode(podcast: Podcast) -> Generator[Episode, None, None]:
    """Create a test episode which whose status is listened-to."""
    episode = Episode(
        podcast=podcast,
        duration=timedelta(hours=1),
        status=Status.LISTENED,
        publication_timestamp=datetime(1, 1, 1, 1, 1, 1),
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


class TestEpisode:
    """Tests for the Episode model."""

    def test_string_repr(self, episode: Episode) -> None:
        """The string representation is "Episode #"."""
        assert str(episode) == f"Episode {episode.episode_number}"

    def test_publication_date(self, episode: Episode) -> None:
        """The date is extracted from the publication timestamp."""
        assert episode.publication_date == datetime(1, 1, 1)

    @pytest.mark.parametrize(
        "expected_image_url,set_image_url",
        [
            ("http://podcast-image-url.com", False),
            ("http://episode-image-url.com", True),
        ],
    )
    def test_episode_image_fallback(
        self, episode: Episode, expected_image_url: str, set_image_url: bool
    ) -> None:
        """The image falls back to podcast, unless it is set explicitly."""
        if set_image_url:
            episode.image_url = expected_image_url
        assert episode.image_url == expected_image_url
