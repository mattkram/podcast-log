import threading

from django.shortcuts import render
from django.views import generic

from .models import Podcast, Episode, EpisodeTable
from .tasks import update_podcast_feed


class PodcastListView(generic.ListView):
    template_name = "index.html"

    def get_queryset(self):
        """Return a list of all podcasts."""
        return Podcast.objects.order_by("title")


class PodcastDetailView(generic.DetailView):
    model = Podcast
    template_name = "podcast_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        episodes = Episode.objects.filter(podcast=context["podcast"]).order_by(
            "-publication_date"
        )
        table = EpisodeTable(episodes)
        table.paginate(page=self.request.GET.get("page", 1), per_page=25)
        context["table"] = table
        return context


class EpisodeListView(generic.TemplateView):
    template_name = "episode_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        episodes = Episode.objects.order_by("-publication_date")
        table = EpisodeTable(episodes)
        table.paginate(page=self.request.GET.get("page", 1), per_page=25)
        context["table"] = table
        return context


def update_podcasts(request):
    """View to update the podcast record."""
    for podcast in Podcast.objects.all():
        thread = threading.Thread(
            target=update_podcast_feed, args=(podcast.id,), daemon=True
        )
        thread.start()
    return render(request, "updating.html")
