import pytest

from podcast_log.models import Podcast, Episode


@pytest.mark.django_db(transaction=True)
def test_podcast_statistics():
    podcast = Podcast(title="Podcast title")
    assert podcast is not None

    assert podcast.title == "Podcast title"
    assert podcast.statistics.num_episodes == 0
    assert podcast.statistics.num_listened == 0

    with pytest.raises(AttributeError):
        assert podcast.statistics.num_non_existent

    # episode = Episode(podcast=podcast, status=Episode.LISTENED)
    #
    # assert episode.status == Episode.LISTENED
    # assert podcast.statistics.num_listened == 1
