from datetime import timedelta, datetime
from typing import Optional

from django.db import models


class Podcast(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    image_url = models.URLField()
    summary = models.CharField(max_length=500)
    last_refreshed = models.DateTimeField(default=datetime(1, 1, 1))
    refresh_interval = models.DurationField(default=timedelta(hours=1))
    episode_number_pattern = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title

    @property
    def needs_update(self):
        update_after = self.last_refreshed + self.refresh_interval
        return update_after <= datetime.now()

    @property
    def episodes(self):
        return Episode.objects.filter(podcast=self)

    @property
    def statistics(self):
        """dict: A dictionary containing podcast statistics."""
        num_episodes = len(self.episodes)
        num_skipped = len(self.episodes.filter(status=Episode.SKIPPED))
        num_ignored = len(self.episodes.filter(status=Episode.IGNORED))
        num_listened = len(self.episodes.filter(status=Episode.LISTENED))
        num_in_progress = len(self.episodes.filter(status=Episode.IN_PROGRESS))
        num_queued = len(self.episodes.filter(status=Episode.QUEUED))
        num_to_listen = num_episodes - num_skipped - num_ignored
        progress_str = (
            f"{num_listened} / {num_to_listen} "
            f"({100 * num_listened / num_to_listen:0.1f}%)"
        )
        time_listened = timedelta(seconds=0)
        for e in self.episodes.filter(status=Episode.LISTENED):
            if e.duration is not None:
                time_listened += e.duration

        dict_ = {
            "num_episodes": num_episodes,
            "num_skipped": num_skipped,
            "num_ignored": num_ignored,
            "num_listened": num_listened,
            "num_in_progress": num_in_progress,
            "num_queued": num_queued,
            "progress": progress_str,
            "time_listened": time_listened,
        }
        return dict_


class Episode(models.Model):
    podcast: Podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    title: str = models.CharField(max_length=200, blank=True)
    publication_timestamp: Optional[datetime] = models.DateTimeField(null=True)
    audio_url: str = models.URLField(max_length=500, blank=True)
    _image_url: str = models.URLField(max_length=500, blank=True)
    description: str = models.CharField(max_length=5000, blank=True)
    duration: Optional[timedelta] = models.DurationField(null=True)
    episode_number: Optional[int] = models.IntegerField(null=True)

    LISTENED = "L"
    IGNORED = "I"
    SKIPPED = "S"
    IN_PROGRESS = "P"
    QUEUED = "Q"
    STATUS_CHOICES = (
        (QUEUED, "Queued"),
        (LISTENED, "Listened"),
        (IN_PROGRESS, "In Progress"),
        (SKIPPED, "Skipped"),
        (IGNORED, "Ignored"),
    )
    status: str = models.CharField(max_length=1, choices=STATUS_CHOICES, default=QUEUED)

    class Meta:
        unique_together = ("podcast", "episode_number")

    def __str__(self):
        return f"Episode {self.episode_number}"

    @property
    def publication_date(self):
        t = self.publication_timestamp
        if t is None:
            return None
        return datetime(year=t.year, month=t.month, day=t.day)

    @property
    def image_url(self):
        """str: Read-only property returning episode image URL, defaulting to podcast image if episode image missing."""
        if not self._image_url:
            return self.podcast.image_url
        return self._image_url

    @image_url.setter
    def image_url(self, value):
        self._image_url = value
