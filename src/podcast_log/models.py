from datetime import timedelta, datetime

import django_tables2 as tables
from django.db import models


class Podcast(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    image_url = models.URLField()
    summary = models.CharField(max_length=200)
    last_refreshed = models.DateTimeField(default=datetime(1, 1, 1))
    refresh_interval = models.DurationField(default=timedelta(hours=1))

    def __str__(self):
        return self.title

    @property
    def needs_update(self):
        update_after = self.last_refreshed + self.refresh_interval
        return update_after <= datetime.now()

    @property
    def episode_table(self):
        return EpisodeTable(self.episode_set.all())


class Episode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    publication_date = models.DateTimeField(null=True)
    audio_url = models.URLField()
    image_url = models.URLField()
    description = models.CharField(max_length=500)
    duration = models.DurationField(null=True)
    episode_number = models.IntegerField(null=True)

    def __str__(self):
        return f"Episode {self.episode_number}"


class EpisodeTable(tables.Table):
    class Meta:
        model = Episode
        fields = (
            "image_url",
            "episode_number",
            "publication_date",
            "duration",
            "description",
        )

    image_url = tables.TemplateColumn(
        '<img src="{{record.image_url}}" style="width: 100px"> ', verbose_name=""
    )
