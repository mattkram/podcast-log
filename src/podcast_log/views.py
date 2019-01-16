from django.views import generic

from .models import Podcast


class IndexView(generic.ListView):
    template_name = "index.html"

    def get_queryset(self):
        """Return a list of all podcasts."""
        return Podcast.objects.order_by("title")


class DetailView(generic.DetailView):
    model = Podcast
    template_name = "podcast_detail.html"
