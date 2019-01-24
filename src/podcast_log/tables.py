import django_tables2 as tables

from podcast_log.models import Episode


def get_episode_class(record):
    """Return a CSS class string name for the table rows, based on episode status."""
    class_str = record.get_status_display().lower()
    return f"row-episode-{'-'.join(class_str.split())}"


option_string = "\n".join(
    (
        "<option "
        f' value="{short}" '
        f' {{% if record.status == "{short}" %}}selected{{% endif %}}'
        ">"
        f"{long}"
        "</option>"
    )
    for short, long in Episode.STATUS_CHOICES
)


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
    podcast = tables.TemplateColumn(
        "<a href=\"{% url 'podcast-detail' record.podcast.id %}\">{{ record.podcast }}</a>",
        verbose_name="Podcast",
    )
    publication_timestamp = tables.TemplateColumn(
        "{{ record.publication_timestamp.date }}", verbose_name="Date"
    )
    status = tables.TemplateColumn(
        """<div class="form-group">
            <select name="status-episode-{{ record.id }}"
                    class="form-control"
                    id="id_status_episode_{{ record.id }}"
                    onchange="this.form.submit()">
        """
        + option_string
        + """
            </select>
        </div>
        """
    )
    edit = tables.TemplateColumn(
        "<a href=\"{% url 'edit-episode' record.id %}\">(Edit)</a>", verbose_name=""
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
