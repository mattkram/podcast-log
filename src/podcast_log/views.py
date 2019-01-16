from django.views import generic

from .models import Podcast, Episode, EpisodeTable


class PodcastListView(generic.ListView):
    template_name = "index.html"

    def get_queryset(self):
        """Return a list of all podcasts."""
        return Podcast.objects.order_by("title")


class PodcastDetailView(generic.DetailView):
    model = Podcast
    template_name = "podcast_detail.html"


class EpisodeListView(generic.TemplateView):
    template_name = "episode_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        episodes = Episode.objects.order_by("-publication_date")
        context["table"] = EpisodeTable(episodes)
        return context
