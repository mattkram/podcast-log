import pytest
from flask import Flask

from podcast_log.models import Podcast, Episode, Status


def test_podcast_statistics(app: Flask) -> None:

    podcast = Podcast(title="Podcast title")
    podcast.save()
    assert podcast is not None

    assert podcast.title == "Podcast title"
    assert podcast.statistics.num_episodes == 0
    assert podcast.statistics.num_listened == 0

    with pytest.raises(AttributeError):
        assert podcast.statistics.num_non_existent

    episode = Episode(podcast=podcast, status=Status.LISTENED)
    episode.save()

    assert episode.status == Status.LISTENED
    assert podcast.statistics.num_listened == 1
