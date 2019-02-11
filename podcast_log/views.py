from flask import Blueprint, render_template, redirect, url_for, request

from .forms import AddPodcastForm, EditPodcastForm  # , EditEpisodeForm
from .models import Podcast, Episode, STATUS_CHOICES
from .tables import PodcastEpisodesTable
from .tasks import create_new_podcast, add_podcast_to_update_queue

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return redirect(url_for("main.podcast_list"))


@bp.route("/podcasts")
def podcast_list():
    podcasts = Podcast.query.order_by(Podcast.title).all()
    return render_template("index.html", podcasts=podcasts)


@bp.route("/b")
def episode_list():
    return render_template("index.html")


@bp.route("/c")
def update_all():
    return render_template("index.html")


@bp.route("/podcasts/add", methods=("GET", "POST"))
def add_podcast():
    form = AddPodcastForm()
    if form.validate_on_submit():
        podcast = create_new_podcast(form.url.data, form.episode_number_pattern.data)
        return redirect(url_for("main.podcast_detail", podcast_id=podcast.id))
    return render_template("add-podcast.html", form=form)


EPISODES_PER_PAGE = 20


@bp.route("/podcast/<int:podcast_id>")
def podcast_detail(podcast_id):
    podcast = Podcast.query.get(podcast_id)
    page = request.args.get("page", 1, type=int)
    episodes = podcast.episodes.paginate(page, EPISODES_PER_PAGE, False)
    table = PodcastEpisodesTable(episodes.items)
    return render_template("podcast-detail.html", podcast=podcast, table=table)


@bp.route("/podcast/<int:podcast_id>/update")
def update_podcast(podcast_id):
    add_podcast_to_update_queue(podcast_id, force=True)
    return redirect(url_for("main.podcast_detail", podcast_id=podcast_id))


@bp.route("/podcast/<int:podcast_id>/edit", methods=("GET", "POST"))
def edit_podcast(podcast_id):
    podcast = Podcast.query.get(podcast_id)
    form = EditPodcastForm(obj=podcast)
    if form.validate_on_submit():
        podcast = Podcast.query.get(podcast_id)
        form.populate_obj(podcast)
        podcast.save()
        return redirect(url_for("main.podcast_detail", podcast_id=podcast.id))
    return render_template("edit-podcast.html", podcast_id=podcast_id, form=form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     podcast = Podcast.objects.get(id=context["pk"])
    #     episodes = Episode.objects.filter(podcast=podcast)
    #     context["status"] = status = kwargs.get("status", "all")
    #     if status is not None and status.lower() != "all":
    #         episodes = episodes.filter(status=status[0].upper())
    #     table = PodcastEpisodesTable(episodes.order_by("-publication_timestamp"))
    #     table.paginate(page=self.request.GET.get("page", 1), per_page=25)
    #     context["podcast"] = podcast
    #     context["table"] = table
    #     return context


# class EpisodeListView(generic.TemplateView):
#     template_name = "episode-list.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["status"] = status = kwargs.get("status", "all")
#         if status is None or status.lower() == "all":
#             episodes = Episode.objects.all()
#         else:
#             episodes = Episode.objects.filter(status=status[0].upper())
#         table = EpisodeTableBase(episodes.order_by("-publication_timestamp"))
#         table.paginate(page=self.request.GET.get("page", 1), per_page=25)
#         context["table"] = table
#         return context
#
#
# def update_podcast(request, pk):
#     """View to update the podcast record."""
#     add_podcast_to_update_queue(pk, force=True)
#     return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("index")))
#
#
# def update_podcasts(request):
#     """View to update the podcast record."""
#     for podcast in Podcast.objects.all():
#         add_podcast_to_update_queue(podcast.id)
#     return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("index")))
#
#
#
# def edit_podcast(request, pk):
#     podcast = Podcast.objects.get(pk=pk)
#     if request.method == "POST":
#         form = EditPodcastForm(request.POST, instance=podcast)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("podcast-detail", args=(podcast.id,)))
#     else:
#         form = EditPodcastForm(instance=podcast)
#     return render(request, "edit-podcast.html", {"podcast_id": pk, "form": form})
#
#
# def edit_episode(request, pk):
#     episode = Episode.objects.get(pk=pk)
#     if request.method == "POST":
#         form = EditEpisodeForm(request.POST, instance=episode)
#         if form.is_valid():
#             if "episode_save" in request.POST:
#                 form.save()
#             elif "episode_delete" in request.POST:
#                 episode.delete()
#             return HttpResponseRedirect(request.POST.get("next", "/"))
#     else:
#         form = EditEpisodeForm(instance=episode)
#     return render(
#         request,
#         "edit-episode.html",
#         {
#             "episode_id": pk,
#             "form": form,
#             "next_url": request.META.get("HTTP_REFERER", "/"),
#         },
#     )
#
@bp.route("/episodes/<int:episode_id>/update-status/", methods=("POST",))
def update_episode_status(episode_id):
    episode = Episode.query.get(episode_id)
    status = request.form["status"]
    for key, value in STATUS_CHOICES.items():
        if value == status:
            episode.status = key
            episode.save()
    return redirect(request.referrer)


def init_app(app):
    app.register_blueprint(bp)
