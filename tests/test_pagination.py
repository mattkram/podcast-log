import random
from typing import Tuple, Any, List

import pytest
from _pytest.fixtures import FixtureRequest
from flask import Flask

from podcast_log.models import Episode
from podcast_log.pagination import Paginator


EpisodeNumberList = List[int]
ItemsAndEpisodeNumbers = Tuple[List[Any], EpisodeNumberList]


@pytest.fixture()
def base_episode_numbers() -> EpisodeNumberList:
    """Construct a list of episode numbers in random order."""
    base_episode_numbers = list(range(25))
    random.shuffle(base_episode_numbers)
    return base_episode_numbers


@pytest.fixture()
def paginator(app: Flask, base_episode_numbers: EpisodeNumberList) -> Paginator:
    for num in base_episode_numbers:
        episode = Episode(episode_number=num)
        episode.save()
    return Paginator(Episode.query, items_per_page=10)


@pytest.fixture(params=["unsorted", "increasing", "decreasing"])
def items_and_expected_episode_numbers(
    request: FixtureRequest,
    paginator: Paginator,
    base_episode_numbers: EpisodeNumberList,
) -> ItemsAndEpisodeNumbers:
    """A parametrized fixture returning a list of episodes sorted various ways and the episode
    numbers associated with those episodes."""

    # Store keyword args to be passed into Pagination.get_items
    items = {
        "unsorted": paginator.get_items(),
        "increasing": paginator.get_items(order_by=Episode.episode_number),
        "decreasing": paginator.get_items(
            order_by=Episode.episode_number, reverse=True
        ),
    }[request.param]

    expected = {
        "unsorted": base_episode_numbers,
        "increasing": sorted(base_episode_numbers),
        "decreasing": sorted(base_episode_numbers, reverse=True),
    }[request.param][: paginator.items_per_page]

    return items, expected


def test_sorting(items_and_expected_episode_numbers: ItemsAndEpisodeNumbers) -> None:
    """The paginator can return items unsorted, or in increasing or decreasing order."""
    items, expected_episode_numbers = items_and_expected_episode_numbers
    assert [item.episode_number for item in items] == expected_episode_numbers
