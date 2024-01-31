"""API route definitions."""

from __future__ import annotations

from flask import Blueprint, Flask, Response, jsonify

from podcast_log.models import Episode, Podcast
from podcast_log.schemata import EpisodeSchema, PodcastSchema

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/podcasts", methods=("GET",))
def get_podcasts() -> Response:
    """Get a list of all podcasts."""
    podcast_objects = Podcast.query.order_by(Podcast.title).all()
    schema = PodcastSchema(many=True)
    podcasts = schema.dump(podcast_objects)
    return jsonify(podcasts)


@bp.route("/podcasts/<int:pk>")
def get_podcast(pk: int) -> tuple[Response, int]:
    """Get a single podcast by ID."""
    podcast_object = Podcast.query.get(pk)
    if podcast_object is None:
        return jsonify({"message": "Podcast could not be found."}), 400

    schema = PodcastSchema()
    podcast = schema.dump(podcast_object)
    return jsonify(podcast), 200


@bp.route("/episodes")
def get_episodes() -> Response:
    """Get a list of all episodes."""
    episode_objects = Episode.query.order_by(Episode.publication_timestamp).all()
    schema = EpisodeSchema(many=True)
    episodes = schema.dump(episode_objects)
    return jsonify(episodes)


@bp.route("/episodes/<int:pk>")
def get_episode(pk: int) -> tuple[Response, int]:
    """Get a single episode by ID."""
    episode_object = Episode.query.get(pk)
    if episode_object is None:
        return jsonify({"message": "Episode could not be found."}), 400

    schema = EpisodeSchema()
    episode = schema.dump(episode_object)
    return jsonify(episode), 200


def init_app(app: Flask) -> None:
    """Initialize API blueprint."""
    app.register_blueprint(bp)
