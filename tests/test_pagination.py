import random
import functools
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


@pytest.fixture(autouse=True)
def episodes(app: Flask, base_episode_numbers: EpisodeNumberList) -> None:
    for num in base_episode_numbers:
        episode = Episode(episode_number=num)
        episode.save()


@pytest.fixture(params=["unsorted", "increasing", "decreasing"])
def items_and_expected_episode_numbers(
    request: FixtureRequest, base_episode_numbers: EpisodeNumberList
) -> ItemsAndEpisodeNumbers:
    """A parametrized fixture returning a list of episodes sorted various ways and the episode
    numbers associated with those episodes."""

    # Use partial to store common arguments to Paginator constructor
    p = functools.partial(Paginator, Episode.query, items_per_page=10)

    # Develop specialized arguments for different cases
    paginator = {
        "unsorted": p(),
        "increasing": p(sort_column=Episode.episode_number),
        "decreasing": p(sort_column=Episode.episode_number, reverse_sort=True),
    }[request.param]

    expected = {
        "unsorted": base_episode_numbers,
        "increasing": sorted(base_episode_numbers),
        "decreasing": sorted(base_episode_numbers, reverse=True),
    }[request.param][: paginator.items_per_page]

    return paginator.items, expected


def test_sorting(items_and_expected_episode_numbers: ItemsAndEpisodeNumbers) -> None:
    """The paginator can return items unsorted, or in increasing or decreasing order."""
    items, expected_episode_numbers = items_and_expected_episode_numbers
    assert [item.episode_number for item in items] == expected_episode_numbers
