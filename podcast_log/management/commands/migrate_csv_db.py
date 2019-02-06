from datetime import datetime
from pathlib import Path

from django.core.exceptions import MultipleObjectsReturned

from podcast_log.models import Podcast, Episode
from podcast_log.tasks import parse_duration
from django.core.management.base import BaseCommand


def get_episode(podcast, episode_number=None, publication_date=None):
    if episode_number is not None:
        try:
            return Episode.objects.get(podcast=podcast, episode_number=episode_number)
        except (MultipleObjectsReturned, Episode.DoesNotExist):
            pass

    if publication_date is not None:
        try:
            episodes = Episode.objects.filter(
                podcast=podcast
            )
            for episode in episodes:
                if episode.publication_date == publication_date:
                    return episode
        except (MultipleObjectsReturned, Episode.DoesNotExist):
            pass

    return Episode(podcast=podcast)


def process_episode(data):

    try:
        podcast = Podcast.objects.get(title__contains=data["podcast"])
    except Podcast.DoesNotExist:
        return

    try:
        data["episode_number"] = int(data.pop("episode_number"))
    except (KeyError, ValueError):
        pass

    try:
        data["duration"] = parse_duration(data["duration"])
    except KeyError:
        pass

    try:
        data["status"] = data["status"][0].upper()
    except KeyError:
        pass

    try:
        data["publication_date"] = datetime.strptime(
            data["publication_date"], "%m/%d/%Y"
        )
    except ValueError:
        data["publication_date"] = datetime.strptime(
            data["publication_date"], "%m/%d/%y"
        )
    except KeyError:
        pass

    filter_dict = {"podcast": podcast}
    for key in ["episode_number", "publication_date"]:
        try:
            filter_dict[key] = data[key]
        except KeyError:
            pass
    # print(filter_dict)

    episode = get_episode(**filter_dict)

    if not episode.title:
        try:
            episode.title = data["title"]
        except KeyError:
            pass

    if episode.duration is None:
        try:
            episode.duration = data["duration"]
        except KeyError:
            pass

    if episode.publication_timestamp is None:
        try:
            episode.publication_timestamp = data["publication_date"]
        except KeyError:
            pass

    if episode.episode_number is None:
        try:
            episode.episode_number = data["episode_number"]
        except KeyError:
            pass

    try:
        episode.status = data["status"]
    except KeyError:
        pass

    print(episode.podcast)
    for field in [
        "title",
        "episode_number",
        "publication_timestamp",
        "duration",
        "status",
    ]:
        print(f"    {field:21s}: {getattr(episode,field)}")

    episode.save()


class Command(BaseCommand):
    help = "Loads existing text-based database."

    def handle(self, *args, **options):
        filename = Path("data") / "Podcast Log All - Episodes.tsv"

        with filename.open() as fp:
            fp.readline()
            for line in fp:
                # Remove blank strings
                data = {}
                for key, value in zip(
                    [
                        "podcast",
                        "episode_number",
                        "status",
                        "duration",
                        "publication_date",
                        "title",
                    ],
                    line.split("\t"),
                ):
                    if value:
                        data[key] = value

                process_episode(data)
