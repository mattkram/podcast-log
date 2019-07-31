"""Define the main routes and views."""
from datetime import timedelta
from typing import Any

from flask import Blueprint, render_template, redirect, url_for, request, Flask
from werkzeug.wrappers import Response

from podcast_log.pagination import Paginator
from .forms import AddPodcastForm, EditPodcastForm, EditEpisodeForm
from .models import Podcast, Episode, STATUS_CHOICES, Status
from .tables import PodcastEpisodesTable, AllEpisodesTable, StatisticsTable
from .tasks import create_new_podcast, add_podcast_to_update_queue

bp = Blueprint("main", __name__)


@bp.route("/")
def index() -> Response:
    """Redirect to the podcast list."""
    return redirect(url_for("main.podcast_list"))


@bp.route("/podcasts")
def podcast_list() -> str:
    """Display a list of podcasts."""
    podcasts = Podcast.query.order_by(Podcast.title).all()
    return render_template("index.html", podcasts=podcasts)


@bp.route("/podcasts/update")
def update_all() -> Response:
    """Update all podcasts."""
    for podcast in Podcast.query.all():
        add_podcast_to_update_queue(podcast.id)
    return redirect(url_for("main.podcast_list"))


@bp.route("/podcasts/add", methods=("GET", "POST"))
def add_podcast() -> Any:
    """Add a new podcast."""
    form = AddPodcastForm()
    if form.validate_on_submit():
        podcast = create_new_podcast(form.url.data, form.episode_number_pattern.data)
        return redirect(url_for("main.podcast_detail", podcast_id=podcast.id))
    return render_template("add-podcast.html", form=form)


@bp.route("/podcast/<int:podcast_id>")
def podcast_detail(podcast_id: int) -> str:
    """Show the details for a single podcast."""
    page = request.args.get("page", 1, type=int)
    status = request.args.get("status")

    podcast = Podcast.query.get(podcast_id)
    query = podcast.episodes
    if status:
        query = query.filter_by(status=getattr(Status, status.upper()))

    paginator = Paginator(
        query, page=page, sort_column=Episode.publication_timestamp, reverse_sort=True
    )
    table = PodcastEpisodesTable(paginator.items)
    return render_template(
        "podcast-detail.html", podcast=podcast, paginator=paginator, table=table
    )


@bp.route("/podcast/<int:podcast_id>/update")
def update_podcast(podcast_id: int) -> Response:
    """Force update a single podcast."""
    add_podcast_to_update_queue(podcast_id, force=True)
    return redirect(url_for("main.podcast_detail", podcast_id=podcast_id))


@bp.route("/podcast/<int:podcast_id>/edit", methods=("GET", "POST"))
def edit_podcast(podcast_id: int) -> Any:
    """Edit the details for a podcast."""
    podcast = Podcast.query.get(podcast_id)
    form = EditPodcastForm(obj=podcast)
    if form.validate_on_submit():
        podcast = Podcast.query.get(podcast_id)
        form.populate_obj(podcast)
        podcast.save()
        return redirect(url_for("main.podcast_detail", podcast_id=podcast.id))
    return render_template("edit-podcast.html", podcast_id=podcast_id, form=form)


@bp.route("/episodes")
def episode_list() -> str:
    """Show a list of the most recent episodes."""
    page = request.args.get("page", 1, type=int)
    status = request.args.get("status")

    query = Episode.query
    if status:
        query = query.filter_by(status=getattr(Status, status.upper()))

    paginator = Paginator(
        query, page=page, sort_column=Episode.publication_timestamp, reverse_sort=True
    )
    table = AllEpisodesTable(paginator.items)
    return render_template("episode-list.html", paginator=paginator, table=table)


@bp.route("/episode/<int:episode_id>/edit", methods=("GET", "POST"))
def edit_episode(episode_id: int) -> Any:
    """Edit an episodes' details."""
    episode = Episode.query.get(episode_id)
    form = EditEpisodeForm(obj=episode)
    if form.validate_on_submit():
        podcast_id = episode.podcast.id
        if "episode_delete" in request.form:
            episode.delete()
        else:
            form.populate_obj(episode)
            episode.save()
        return redirect(url_for("main.podcast_detail", podcast_id=podcast_id))
    return render_template("edit-episode.html", episode_id=episode_id, form=form)


@bp.route("/episode/<int:episode_id>/update-status", methods=("POST",))
def update_episode_status(episode_id: int) -> Response:
    """Update the status of a specific episode."""
    episode = Episode.query.get(episode_id)
    status = request.form["status"]
    for key, value in STATUS_CHOICES.items():
        if value == status:
            episode.status = key
            episode.save()
    return redirect(request.referrer)


@bp.route("/statistics")
def statistics() -> str:
    """Show the  overall statistics for each podcast and the cumulative totals."""
    podcasts = Podcast.query.order_by(Podcast.title).all()
    total_progress = ""
    total_time_listened = timedelta(seconds=0)
    for podcast in podcasts:
        total_time_listened += podcast.statistics.time_listened

    items = []
    for podcast in podcasts:
        items.append(
            {
                "image_url": podcast.image_url,
                "title": podcast.title,
                "progress": podcast.statistics.progress,
                "time_listened": podcast.statistics.time_listened,
            }
        )
    items.append(
        {
            "image_url": "",
            "title": "Total",
            "progress": total_progress,
            "time_listened": total_time_listened,
        }
    )
    table = StatisticsTable(items)
    return render_template("statistics.html", table=table)


def init_app(app: Flask) -> None:
    """Initialize the application routes by registering the blueprint."""
    app.register_blueprint(bp)
