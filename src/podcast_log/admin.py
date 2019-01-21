from django.contrib import admin

from .models import Podcast, Episode


class EpisodeAdmin(admin.ModelAdmin):
    list_display = (
        "podcast",
        "episode_number",
        "title",
        "publication_timestamp",
        "duration",
        "status",
    )
    list_filter = ("podcast",)


admin.site.register(Podcast)
admin.site.register(Episode, EpisodeAdmin)
