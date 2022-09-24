"""Background tasks for updating podcast feeds."""
from __future__ import annotations

import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from queue import Queue
from threading import Thread
from typing import Any

import feedparser
from flask import current_app
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from podcast_log.models import Episode, Podcast, Status

# TODO: Refactor to combine some functionality in update and add functions
# TODO: Consider update_or_create when updating episodes


def _update_queued_podcasts(q: Queue) -> None:
    """Infinite loop that will update podcasts in a queue in worker thread."""
    while True:
        app, podcast_id, force = q.get()
        with app.app_context():
            update_podcast_feed(podcast_id, force=force)
        q.task_done()


queue: Queue = Queue()
update_thread = Thread(target=_update_queued_podcasts, args=(queue,), daemon=True)
update_thread.start()


def add_podcast_to_update_queue(podcast_id: int, force: bool = False) -> None:
    """Queue a podcast to be updated."""
    # noinspection PyProtectedMember
    queue.put((current_app._get_current_object(), podcast_id, force))  # type: ignore


def update_podcast_feed(podcast_id: int, force: bool = False) -> None:
    """Update a podcast by parsing its RSS feed."""
    logger = current_app.logger
    podcast = Podcast.query.get(podcast_id)

    if not podcast.needs_update and not force:
        logger.info(f"Podcast {podcast} has been updated recently, doesn't need update")
        return

    dict_ = feedparser.parse(podcast.url)

    logger.info(f"Loading podcast {podcast} from {podcast.url}")
    logger.info(f"  Parsing {len(dict_['entries'])} entries")
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

        logger.info(f"Saving episode: {podcast}, {episode}")
        episode.save()

    podcast.last_refreshed = datetime.now()
    podcast.save()

    logger.info("Completed loading podcast")


def create_new_podcast(feed_url: str, episode_number_pattern: str = None) -> Podcast:
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


def get_episode(
    podcast: Podcast, episode_number: int = None, publication_date: datetime = None
) -> Episode:
    """Find a matching episode, or create a new one."""
    # Try to find an episode by episode number first
    if episode_number is not None:
        episode = Episode.query.filter_by(
            podcast=podcast, episode_number=episode_number
        ).first()
        if episode is not None:
            return episode

    # Then try to find the episode by publication date
    if publication_date is not None:
        episode = Episode.query.filter_by(
            podcast=podcast, publication_date=publication_date
        ).first()
        if episode is not None:
            return episode

    # Otherwise, create a new episode
    return Episode(podcast=podcast)


def find_podcast_containing(podcast_title: str) -> Podcast:
    """Find the podcast whose title contains the provided text."""
    try:
        return Podcast.query.filter(Podcast.title.contains(podcast_title)).one()
    except NoResultFound:
        print(f"No podcast found containing {podcast_title}, skipping")
        raise
    except MultipleResultsFound:
        print(
            f"Multiple results found for podcast containing {podcast_title}, skipping"
        )
        raise


def update_episode_data(episode: "Episode", episode_data: dict[str, Any]) -> None:
    """Update the attributes of an episode from a dictionary without overwriting existing values."""
    for key, value in episode_data.items():
        old_value = getattr(episode, key)
        if not old_value:
            try:
                setattr(episode, key, value)
            except AttributeError:
                print(episode, key, value)

    if "status" in episode_data:
        episode.status = getattr(Status, episode_data["status"])

    episode.save()


def process_episode(episode_data: dict[str, Any]) -> None:
    """Given the input data, try to find a matching episode to update the status.

    Otherwise, add to the database.

    """
    podcast_title = episode_data.pop("podcast")
    podcast = find_podcast_containing(podcast_title)

    filter_dict = {"podcast": podcast}
    for key in ["episode_number", "publication_date"]:
        if key in episode_data:
            filter_dict[key] = episode_data[key]
    # print(filter_dict)

    episode = get_episode(**filter_dict)

    update_episode_data(episode, episode_data)


def clean_episode_data(episode_data: dict[str, Any]) -> dict[str, Any]:
    """Perform data conversions."""
    try:
        episode_data["episode_number"] = int(episode_data.pop("episode_number"))
    except (KeyError, ValueError):
        pass

    try:
        episode_data["duration"] = parse_duration(episode_data["duration"])
    except KeyError:
        pass
    try:
        episode_data["status"] = episode_data["status"].upper().replace(" ", "_")
    except KeyError:
        pass

    try:
        episode_data["publication_timestamp"] = datetime.strptime(
            episode_data["publication_timestamp"], "%m/%d/%Y"
        )
    except ValueError:
        episode_data["publication_timestamp"] = datetime.strptime(
            episode_data["publication_timestamp"], "%m/%d/%y"
        )
    except KeyError:
        pass
    return episode_data


def migrate_csv_file(filename: Path) -> None:
    """Migrate from TSV file loaded from Google Sheets. Use TSV since some values have commas."""
    with filename.open() as fp:
        fp.readline()  # Read first line to skip header
        for line in fp:
            # Construct a data dict for the row, skipping blanks
            data = {}
            for key, value in zip(
                [
                    "podcast",
                    "episode_number",
                    "status",
                    "duration",
                    "publication_timestamp",
                    "title",
                ],
                line.split("\t"),
            ):
                if value:
                    data[key] = value

            try:
                process_episode(clean_episode_data(data))
            except (NoResultFound, MultipleResultsFound):
                pass
