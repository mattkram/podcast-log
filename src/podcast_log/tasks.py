import logging
import time
from datetime import timedelta, datetime

import feedparser

from .models import Podcast, Episode

logger = logging.getLogger("django")


def update_podcast_feed(podcast_id):
    podcast = Podcast.objects.get(id=podcast_id)

    if not podcast.needs_update:
        logger.info(
            "Podcast %s has been updated recently, doesn't need update", podcast
        )
        return

    dict_ = feedparser.parse(podcast.url)

    logger.info("Loading podcast '%s' from '%s'", podcast, podcast.url)
    logger.info("  Parsing %d entries", len(dict_["entries"]))
    logger.debug(dict_["feed"])

    for episode_dict in dict_["entries"]:
        publication_date = convert_structured_time(episode_dict["published_parsed"])

        if publication_date <= podcast.last_refreshed:
            break  # Break out of loop once older episodes are reached

        episode, created = Episode.objects.get_or_create(
            podcast=podcast, publication_date=publication_date
        )

        episode.title = episode_dict["title"]
        episode.description = episode_dict["description"]
        episode.duration = parse_duration(episode_dict["itunes_duration"])
        episode.image_url = episode_dict["image"]["href"]
        episode.episode_number = episode_dict.get("itunes_episode")

        episode.save()
        logger.info("Saving episode: %s, %s", podcast, episode)

    podcast.last_refreshed = datetime.now()
    podcast.save()

    logger.info("Completed loading podcast")


def convert_structured_time(structured_time: time.struct_time) -> datetime:
    """Convert a structured time object into a datetime object."""
    return datetime.fromtimestamp(time.mktime(structured_time))


def parse_duration(string: str) -> timedelta:
    """Parse a string into a duration object.

    String can be of the form HH:MM:SS or MM:SS.

    Args:
        string: String to parse.

    Returns:
        A timedelta object.

    """
    parts = [int(i) for i in string.split(":")[::-1]]  # s, m, [h]
    kwargs = dict(zip(["seconds", "minutes", "hours"], parts))
    return timedelta(**kwargs)
