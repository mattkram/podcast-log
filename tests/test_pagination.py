import random
from functools import partial
from typing import Any, List, Callable

import pytest

from podcast_log.models import Episode
from podcast_log.pagination import Paginator

EpisodeNumberList = List[int]


@pytest.fixture()
def episode_numbers() -> EpisodeNumberList:
    """Construct a list of episode numbers in random order."""
    base_episode_numbers = list(range(25))
    random.shuffle(base_episode_numbers)
    return base_episode_numbers


@pytest.fixture(autouse=True)
def episodes(episode_numbers: EpisodeNumberList) -> None:
    for num in episode_numbers:
        episode = Episode(episode_number=num)
        episode.save()


@pytest.mark.parametrize(
    "kwargs,sort_func",
    [
        (dict(), lambda x: x),
        (dict(sort_column=Episode.episode_number), sorted),
        (
            dict(sort_column=Episode.episode_number, reverse_sort=True),
            partial(sorted, reverse=True),
        ),
    ],
    ids=["unsorted", "increasing", "decreasing"],
)
def test_sorting(
    episode_numbers: EpisodeNumberList,
    kwargs: Any,
    sort_func: Callable[[EpisodeNumberList], EpisodeNumberList],
) -> None:
    """The paginator can return items unsorted, or in increasing or decreasing order."""
    paginator = Paginator(Episode.query, items_per_page=10, **kwargs)
    expected_episode_numbers = sort_func(episode_numbers)[: paginator.items_per_page]
    assert [item.episode_number for item in paginator.items] == expected_episode_numbers
