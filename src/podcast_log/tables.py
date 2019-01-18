import django_tables2 as tables

from podcast_log.models import Episode


class EpisodeTable(tables.Table):
    class Meta:
        model = Episode
        fields = (
            "image_url",
            "episode_number",
            "title",
            "publication_date",
            "duration",
            "description",
            "status",
        )

    image_url = tables.TemplateColumn(
        '<img src="{{record.image_url}}" style="max-height: 80px"> ', verbose_name=""
    )
    description = tables.TemplateColumn("{{record.description|truncatechars:200}}")
    # description = tables.TemplateColumn("{{record.description|safe}}")
