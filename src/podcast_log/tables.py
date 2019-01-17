import django_tables2 as tables

from podcast_log.models import Episode


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
