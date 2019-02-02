from datetime import timedelta, datetime
from typing import Optional

from django.db import models


class Podcast(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    image_url = models.URLField()
    summary = models.CharField(max_length=2000)
    last_refreshed = models.DateTimeField(default=datetime(1, 1, 1))
    refresh_interval = models.DurationField(default=timedelta(hours=1))
    episode_number_pattern = models.CharField(max_length=50, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.statistics = PodcastStatistics(self)

    def __str__(self):
        return self.title

    @property
    def needs_update(self):
        update_after = self.last_refreshed + self.refresh_interval
        return update_after <= datetime.now()

    @property
    def episodes(self):
        return Episode.objects.filter(podcast=self)


class PodcastStatistics:
    def __init__(self, podcast):
        self.podcast = podcast

    @property
    def num_episodes(self):
        return len(self.podcast.episodes)

    def __getattr__(self, name: str):
        if name.startswith("num_"):
            try:
                status = getattr(Episode, name.replace("num_", "").upper())
            except AttributeError:
                raise AttributeError(
                    f"Attribute {name} cannot be accessed, no associated episode status"
                )
            return len(self.podcast.episodes.filter(status=status))
        return super().__getattribute__(name)

    @property
    def progress(self):
        num_to_listen = self.num_episodes - self.num_ignored
        pct_listened = (
            100 * self.num_listened / num_to_listen if num_to_listen > 0 else 0.0
        )
        return f"{self.num_listened} / {num_to_listen} ({pct_listened:0.1f}%)"

    @property
    def time_listened(self):
        time_listened = timedelta(seconds=0)
        for e in self.podcast.episodes.filter(status=Episode.LISTENED):
            if e.duration is not None:
                time_listened += e.duration
        return time_listened


class Episode(models.Model):
    podcast: Podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    title: str = models.CharField(max_length=200, blank=True)
    publication_timestamp: Optional[datetime] = models.DateTimeField(null=True)
    audio_url: str = models.URLField(max_length=500, blank=True)
    _image_url: str = models.URLField(max_length=500, blank=True)
    description: str = models.CharField(max_length=5000, blank=True)
    duration: Optional[timedelta] = models.DurationField(null=True)
    episode_number: Optional[int] = models.IntegerField(null=True)
    episode_part: int = models.IntegerField(default=1)

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

    needs_review: bool = models.BooleanField(default=False)

    class Meta:
        unique_together = ("podcast", "episode_number", "episode_part")

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
