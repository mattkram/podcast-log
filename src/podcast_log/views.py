import threading

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .forms import AddPodcastForm
from .models import Podcast, Episode
from .tables import EpisodeListTable, PodcastDetailEpisodeTable
from .tasks import update_podcast_feed, create_new_podcast


class PodcastListView(generic.ListView):
    template_name = "index.html"

    def get_queryset(self):
        """Return a list of all podcasts."""
        return Podcast.objects.order_by("title")


class PodcastDetailView(generic.DetailView):
    model = Podcast
    template_name = "podcast-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        episodes = Episode.objects.filter(podcast=context["podcast"]).order_by(
            "-publication_timestamp"
        )
        table = PodcastDetailEpisodeTable(episodes)
        table.paginate(page=self.request.GET.get("page", 1), per_page=25)
        context["table"] = table
        return context


class EpisodeListView(generic.TemplateView):
    template_name = "episode-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        episodes = Episode.objects.order_by("-publication_timestamp")
        table = EpisodeListTable(episodes)
        table.paginate(page=self.request.GET.get("page", 1), per_page=25)
        context["table"] = table
        return context


def update_podcast(request, pk):
    """View to update the podcast record."""
    thread = threading.Thread(
        target=update_podcast_feed, args=(pk,), kwargs={"force": True}, daemon=True
    )
    thread.start()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("index")))


def update_podcasts(request):
    """View to update the podcast record."""
    for podcast in Podcast.objects.all():
        thread = threading.Thread(
            target=update_podcast_feed, args=(podcast.id,), kwargs={"force": True}, daemon=True
        )
        thread.start()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("index")))


def add_podcast(request):
    if request.method == "POST":
        form = AddPodcastForm(request.POST)

        if form.is_valid():
            podcast = create_new_podcast(form.cleaned_data["url"])
            thread = threading.Thread(
                target=update_podcast_feed, args=(podcast.id,), daemon=True
            )
            thread.start()

            return HttpResponseRedirect(reverse("index"))
    else:
        form = AddPodcastForm()

    return render(request, "add-podcast.html", {"form": form})
