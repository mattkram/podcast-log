"""Define the main routes and views."""
from typing import Any

import flask
from flask import Blueprint, redirect, url_for, request, Flask
from werkzeug.wrappers import Response

from .forms import AddPodcastForm, EditPodcastForm, EditEpisodeForm
from .models import Podcast, Episode, STATUS_CHOICES
from .tables import PodcastEpisodesTable
from .tasks import create_new_podcast, add_podcast_to_update_queue

bp = Blueprint("main", __name__)


def render_template(*args: Any, **kwargs: Any) -> Response:
    """Wrap rendered template in a Response object (for mypy)."""
    return Response(flask.render_template(*args, **kwargs))


@bp.route("/")
def index() -> Response:
    """Redirect to the podcast list."""
    return redirect(url_for("main.podcast_list"))


@bp.route("/podcasts")
def podcast_list() -> Response:
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
def add_podcast() -> Response:
    """Add a new podcast."""
    form = AddPodcastForm()
    if form.validate_on_submit():
        podcast = create_new_podcast(form.url.data, form.episode_number_pattern.data)
        return redirect(url_for("main.podcast_detail", podcast_id=podcast.id))
    return render_template("add-podcast.html", form=form)


EPISODES_PER_PAGE = 20


@bp.route("/podcast/<int:podcast_id>")
def podcast_detail(podcast_id: int) -> Response:
    """Show the details for a single podcast."""
    podcast = Podcast.query.get(podcast_id)
    page = request.args.get("page", 1, type=int)
    episodes = podcast.episodes.paginate(page, EPISODES_PER_PAGE, False)
    table = PodcastEpisodesTable(episodes.items)
    return render_template("podcast-detail.html", podcast=podcast, table=table)


@bp.route("/podcast/<int:podcast_id>/update")
def update_podcast(podcast_id: int) -> Response:
    """Force update a single podcast."""
    add_podcast_to_update_queue(podcast_id, force=True)
    return redirect(url_for("main.podcast_detail", podcast_id=podcast_id))


@bp.route("/podcast/<int:podcast_id>/edit", methods=("GET", "POST"))
def edit_podcast(podcast_id: int) -> Response:
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
def episode_list() -> Response:
    """Show a list of the most recent episodes."""
    page = request.args.get("page", 1, type=int)
    episodes = Episode.query.paginate(page, EPISODES_PER_PAGE, False)
    table = PodcastEpisodesTable(episodes.items)
    return render_template("episode-list.html", table=table)


@bp.route("/episode/<int:episode_id>/edit", methods=("GET", "POST"))
def edit_episode(episode_id: int) -> Response:
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


def init_app(app: Flask) -> None:
    """Initialize the application routes by registering the blueprint."""
    app.register_blueprint(bp)
