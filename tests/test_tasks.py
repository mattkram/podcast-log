import feedparser
import pytest
from _pytest.monkeypatch import MonkeyPatch

from podcast_log.models import Podcast
from podcast_log.tasks import create_new_podcast


@pytest.fixture(autouse=True)
def mock_feedparser(monkeypatch: MonkeyPatch) -> None:
    dict_ = {
        "feed": {
            "title": "Podcast title",
            "image": {"href": "http://image-url.com"},
            "description": "Podcast description",
        }
    }
    monkeypatch.setattr(feedparser, "parse", lambda _: dict_)


@pytest.fixture()
def podcast() -> Podcast:
    return create_new_podcast("http://podcast-feed.com/rss", r"(\d+)")


@pytest.mark.parametrize(
    "attr_name,expected_value",
    [
        ("url", "http://podcast-feed.com/rss"),
        ("episode_number_pattern", r"(\d+)"),
        ("image_url", "http://image-url.com"),
        ("title", "Podcast title"),
        ("summary", "Podcast description"),
    ],
)
def test_create_new_podcast(
    podcast: Podcast, attr_name: str, expected_value: str
) -> None:
    value = getattr(podcast, attr_name)
    assert value == expected_value
