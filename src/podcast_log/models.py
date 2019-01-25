from datetime import timedelta, datetime

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


class Episode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    publication_timestamp = models.DateTimeField(null=True)
    audio_url = models.URLField(max_length=500, blank=True)
    _image_url = models.URLField(max_length=500, blank=True)
    description = models.CharField(max_length=5000, blank=True)
    duration = models.DurationField(null=True)
    episode_number = models.IntegerField(null=True)

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
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=QUEUED)

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
