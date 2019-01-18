from datetime import timedelta, datetime

from django.db import models


class Podcast(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    image_url = models.URLField()
    summary = models.CharField(max_length=500)
    last_refreshed = models.DateTimeField(default=datetime(1, 1, 1))
    refresh_interval = models.DurationField(default=timedelta(hours=1))

    def __str__(self):
        return self.title

    @property
    def needs_update(self):
        update_after = self.last_refreshed + self.refresh_interval
        return update_after <= datetime.now()


class Episode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    publication_timestamp = models.DateTimeField(null=True)
    audio_url = models.URLField()
    image_url = models.URLField()
    description = models.CharField(max_length=500)
    duration = models.DurationField(null=True)
    episode_number = models.IntegerField(null=True)

    LISTENED = "L"
    IGNORED = "I"
    SKIPPED = "S"
    IN_PROGRESS = "P"
    QUEUED = "Q"
    STATUS_CHOICES = (
        (LISTENED, "Listened"),
        (IGNORED, "Ignored"),
        (SKIPPED, "Skipped"),
        (IN_PROGRESS, "In Progress"),
        (QUEUED, "Queued"),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=QUEUED)

    def __str__(self):
        return f"Episode {self.episode_number}"
