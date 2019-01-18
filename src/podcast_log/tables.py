import django_tables2 as tables

from podcast_log.models import Episode


class EpisodeListTable(tables.Table):
    class Meta:
        model = Episode
        fields = (
            "image_url",
            "podcast",
            "episode_number",
            "title",
            "publication_timestamp",
            "duration",
            "status",
        )

    image_url = tables.TemplateColumn(
        '<img src="{{ record.image_url }}" class="img-episode-list"> ', verbose_name=""
    )
    podcast = tables.Column(verbose_name="Podcast")
    publication_timestamp = tables.TemplateColumn(
        "{{ record.publication_timestamp.date }}", verbose_name="Date"
    )


class PodcastDetailEpisodeTable(EpisodeListTable):
    class Meta:
        model = Episode
        fields = (
            "image_url",
            "episode_number",
            "title",
            "publication_timestamp",
            "duration",
            "description",
            "status",
        )

    description = tables.TemplateColumn("{{ record.description|truncatechars:200 }}")
    podcast = None
