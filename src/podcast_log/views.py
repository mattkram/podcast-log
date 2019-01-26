import re
import threading

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .forms import AddPodcastForm, EditPodcastForm, EditEpisodeForm
from .models import Podcast, Episode
from .tables import EpisodeListTable, PodcastDetailEpisodeTable
from .tasks import update_podcast_feed, create_new_podcast, add_podcast_to_update_queue


class PodcastListView(generic.ListView):
    template_name = "index.html"

    def get_queryset(self):
        """Return a list of all podcasts."""
        return Podcast.objects.order_by("title")


class PodcastDetailView(generic.TemplateView):
    template_name = "podcast-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        podcast = Podcast.objects.get(id=context["pk"])
        episodes = Episode.objects.filter(podcast=podcast)
        context["status"] = status = kwargs.get("status", "all")
        if status is not None and status.lower() != "all":
            episodes = episodes.filter(status=status[0].upper())
        table = PodcastDetailEpisodeTable(episodes.order_by("-publication_timestamp"))
        table.paginate(page=self.request.GET.get("page", 1), per_page=25)
        context["podcast"] = podcast
        context["table"] = table
        return context


class EpisodeListView(generic.TemplateView):
    template_name = "episode-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = status = kwargs.get("status", "all")
        if status is None or status.lower() == "all":
            episodes = Episode.objects.all()
        else:
            episodes = Episode.objects.filter(status=status[0].upper())
        table = EpisodeListTable(episodes.order_by("-publication_timestamp"))
        table.paginate(page=self.request.GET.get("page", 1), per_page=25)
        context["table"] = table
        return context


def update_podcast(request, pk):
    """View to update the podcast record."""
    add_podcast_to_update_queue(pk, force=True)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("index")))


def update_podcasts(request):
    """View to update the podcast record."""
    for podcast in Podcast.objects.all():
        add_podcast_to_update_queue(podcast.id)
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


def edit_podcast(request, pk):
    podcast = Podcast.objects.get(pk=pk)
    if request.method == "POST":
        form = EditPodcastForm(request.POST, instance=podcast)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                request.META.get("HTTP_REFERER"),
                reverse("podcast-detail", args=(podcast.id,)),
            )
    else:
        form = EditPodcastForm(instance=podcast)
    return render(request, "edit-podcast.html", {"podcast_id": pk, "form": form})


def edit_episode(request, pk):
    episode = Episode.objects.get(pk=pk)
    if request.method == "POST":
        form = EditEpisodeForm(request.POST, instance=episode)
        if form.is_valid():
            if "episode_save" in request.POST:
                form.save()
            elif "episode_delete" in request.POST:
                episode.delete()
            return HttpResponseRedirect(request.POST.get("next", "/"))
    else:
        form = EditEpisodeForm(instance=episode)
    return render(
        request,
        "edit-episode.html",
        {
            "episode_id": pk,
            "form": form,
            "next_url": request.META.get("HTTP_REFERER", "/"),
        },
    )


def update_episode_statuses(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            match = re.match(r"status-episode-(\d+)", key)
            if match:
                episode_id = int(match.group(1))
                episode = Episode.objects.get(id=episode_id)
                if episode.status != value:
                    episode.status = value
                    episode.save()

    return HttpResponseRedirect(
        request.META.get("HTTP_REFERER", reverse("episode-list"))
    )
