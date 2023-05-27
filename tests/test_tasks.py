from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

import feedparser
import pytest

import podcast_log.tasks
from podcast_log.models import Episode, Podcast, Status
from podcast_log.tasks import create_new_podcast, update_podcast_feed

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch


@pytest.fixture(autouse=True)
def mock_feedparser(monkeypatch: MonkeyPatch) -> None:
    dict_ = {
        "feed": {
            "title": "Podcast title",
            "image": {"href": "http://podcast-image.com"},
            "description": "Podcast description",
        },
        "entries": [
            {
                "title": "Episode title",
                "description": "Episode description",
                "published_parsed": (2001, 2, 3, 4, 0, 1, 5, 250, 0),
                "image": {"href": "http://episode-image.com"},
                "itunes_duration": "2:30:40",
                "itunes_episode": 39,
            }
        ],
    }
    monkeypatch.setattr(feedparser, "parse", lambda _: dict_)


@pytest.fixture(autouse=True)
def disable_update_queue(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        podcast_log.tasks, "add_podcast_to_update_queue", lambda *_: None
    )


@pytest.fixture()
def podcast() -> Podcast:
    return create_new_podcast("http://podcast-feed.com/rss", r"(\d+)")


@pytest.mark.parametrize(
    "attr_name,expected_value",
    [
        ("url", "http://podcast-feed.com/rss"),
        ("episode_number_pattern", r"(\d+)"),
        ("image_url", "http://podcast-image.com"),
        ("title", "Podcast title"),
        ("summary", "Podcast description"),
    ],
)
def test_create_new_podcast(
    podcast: Podcast, attr_name: str, expected_value: str
) -> None:
    value = getattr(podcast, attr_name)
    assert value == expected_value


@pytest.fixture()
def episode(podcast: Podcast) -> Episode:
    update_podcast_feed(podcast.id, force=True)
    return list(podcast.episodes)[0]


@pytest.mark.parametrize(
    "attr_name,expected_value",
    [
        ("title", "Episode title"),
        ("publication_timestamp", datetime(2001, 2, 3, 4, 0, 1)),
        ("image_url", "http://episode-image.com"),
        ("description", "Episode description"),
        ("duration", timedelta(hours=2, minutes=30, seconds=40)),
        ("episode_number", 39),
        ("episode_part", 1),
        ("status", Status.QUEUED),
        ("needs_review", False),
    ],
)
def test_update_podcast_feed(
    episode: Episode, attr_name: str, expected_value: Any
) -> None:
    value = getattr(episode, attr_name)
    assert value == expected_value
