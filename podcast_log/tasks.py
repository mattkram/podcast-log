import re
import time
from datetime import timedelta, datetime
from queue import Queue
from threading import Thread
from typing import Optional

import feedparser
from flask import current_app
from sqlalchemy.orm.exc import NoResultFound

from .models import Podcast, Episode


# TODO: Refactor to combine some functionality in update and add functions
# TODO: Consider update_or_create when updating episodes


def _update_queued_podcasts(q):
    """Infinite loop that will update podcasts in a queue in worker thread."""
    while True:
        app, podcast_id, force = q.get()
        with app.app_context():
            update_podcast_feed(podcast_id, force=force)
        q.task_done()


queue = Queue()
update_thread = Thread(target=_update_queued_podcasts, args=(queue,), daemon=True)
update_thread.start()


def add_podcast_to_update_queue(podcast_id, force=False):
    # noinspection PyProtectedMember
    queue.put((current_app._get_current_object(), podcast_id, force))


def update_podcast_feed(podcast_id, force=False):
    logger = current_app.logger
    podcast = Podcast.query.get(podcast_id)

    if not podcast.needs_update and not force:
        logger.info(
            "Podcast %s has been updated recently, doesn't need update", podcast
        )
        return

    dict_ = feedparser.parse(podcast.url)

    logger.info("Loading podcast '%s' from '%s'", podcast, podcast.url)
    logger.info("  Parsing %d entries", len(dict_["entries"]))
    logger.debug(dict_["feed"])

    # Create a list of new entries, unless forced to process all entries
    if force:
        entries = dict_["entries"]
    else:
        entries = [
            e
            for e in dict_["entries"]
            if convert_structured_time(e["published_parsed"]) > podcast.last_refreshed
        ]

    for episode_dict in entries[::-1]:
        publication_timestamp = convert_structured_time(
            episode_dict["published_parsed"]
        )

        try:
            episode = Episode.query.filter_by(
                podcast=podcast, publication_timestamp=publication_timestamp
            ).one()
        except NoResultFound:
            episode = Episode(
                podcast=podcast, publication_timestamp=publication_timestamp
            )

        episode.title = episode_dict.get("title", "")
        episode.description = episode_dict.get("description", "")
        episode.duration = parse_duration(episode_dict.get("itunes_duration", "0:0"))
        try:
            episode.image_url = episode_dict["image"]["href"]
        except KeyError:
            pass

        try:
            episode.episode_number = episode_dict["itunes_episode"]
        except KeyError:
            try:
                match = re.search(podcast.episode_number_pattern, episode_dict["title"])
            except TypeError:
                pass  # No pattern defined
            else:
                if match:
                    episode.episode_number = int(match.group(1))

        # try:
        episode.save()
        # except IntegrityError:
        #     episode.needs_review = True
        #     episode.episode_number = None
        #     episode.save()

        logger.info("Saving episode: %s, %s", podcast, episode)

    podcast.last_refreshed = datetime.now()
    podcast.save()

    logger.info("Completed loading podcast")


def create_new_podcast(
    feed_url: str, episode_number_pattern: str = None
) -> Optional[Podcast]:
    """If a podcast doesn't already exist with the same feed URL, create it by parsing the feed."""
    # If the podcast already exists, return out of this function, else continue/pass
    try:
        podcast = Podcast.query.filter_by(url=feed_url).one()
    except NoResultFound:
        pass
    else:
        return podcast

    podcast = Podcast(url=feed_url)

    if episode_number_pattern:
        podcast.episode_number_pattern = episode_number_pattern

    dict_ = feedparser.parse(feed_url)
    feed = dict_["feed"]

    podcast = Podcast()
    podcast.title = feed["title"]
    podcast.image_url = feed["image"]["href"]
    podcast.summary = feed["description"]

    podcast.save()

    add_podcast_to_update_queue(podcast.id)

    return podcast


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
