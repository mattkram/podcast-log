import django_tables2 as tables

from podcast_log.models import Episode


def get_episode_class(record):
    """Return a CSS class string name for the table rows, based on episode status."""
    class_str = record.get_status_display().lower()
    return f"row-episode-{'-'.join(class_str.split())}"


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
        row_attrs = {"class": get_episode_class}

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
        row_attrs = {"class": get_episode_class}

    description = tables.TemplateColumn("{{ record.description|truncatechars:200 }}")
    podcast = None
