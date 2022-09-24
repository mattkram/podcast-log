import pytest
from flask import Response
from flask.testing import FlaskClient
from marshmallow import Schema

from podcast_log.models import Episode, Podcast
from podcast_log.schemata import EpisodeSchema, PodcastSchema


@pytest.fixture()
def get_podcasts_response(client: FlaskClient) -> Response:
    return client.get("/api/podcasts")


def test_get_podcasts_status_200(get_podcasts_response: Response) -> None:
    assert get_podcasts_response.status_code == 200


def test_get_podcasts_data(get_podcasts_response: Response) -> None:
    json_data = get_podcasts_response.get_json()
    assert len(json_data) == len(Podcast.query.all())


@pytest.mark.parametrize("podcast_id, expected_status_code", [(1, 200), (200, 400)])
def test_get_podcast_status_codes(
    client: FlaskClient, podcast_id: int, expected_status_code: int
) -> None:
    response = client.get(f"/api/podcasts/{podcast_id}")
    assert response.status_code == expected_status_code


@pytest.fixture()
def get_episodes_response(client: FlaskClient) -> Response:
    return client.get("/api/episodes")


def test_get_episodes_status_200(get_episodes_response: Response) -> None:
    assert get_episodes_response.status_code == 200


def test_get_episodes_data(get_episodes_response: Response) -> None:
    json_data = get_episodes_response.get_json()
    assert len(json_data) == len(Episode.query.all())


@pytest.mark.parametrize(
    "episode_id, expected_status_code", [(1, 200), (2, 200), (3, 200), (200, 400)]
)
def test_get_episode_status_codes(
    client: FlaskClient, episode_id: int, expected_status_code: int
) -> None:
    response = client.get(f"/api/episodes/{episode_id}")
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "url, schema, many",
    [
        ("/api/episodes/1", EpisodeSchema(), False),
        ("/api/episodes", EpisodeSchema(), True),
        ("/api/podcasts/1", PodcastSchema(), False),
        ("/api/podcasts", PodcastSchema(), True),
    ],
)
def test_get_requests_match_schema(
    client: FlaskClient, url: str, schema: Schema, many: bool
) -> None:
    response = client.get(url)
    json_data = response.get_json()
    assert schema.validate(data=json_data, many=many)
