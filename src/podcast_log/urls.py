from django.urls import path

from . import views

urlpatterns = [
    path("", views.PodcastListView.as_view(), name="index"),
    path("podcasts/", views.PodcastListView.as_view(), name="podcast-list"),
    path("podcasts/update/", views.update_podcasts, name="update-all"),
    path("podcasts/add/", views.add_podcast, name="add-podcast"),
    path("podcast/<int:pk>/", views.PodcastDetailView.as_view(), name="podcast-detail"),
    path(
        "podcast/<int:pk>/status=<str:status>/",
        views.PodcastDetailView.as_view(),
        name="podcast-detail",
    ),
    path("podcast/<int:pk>/update/", views.update_podcast, name="update-podcast"),
    path("podcast/<int:pk>/edit/", views.edit_podcast, name="edit-podcast"),
    path("episodes/", views.EpisodeListView.as_view(), name="episode-list"),
    path(
        "episodes/status=<str:status>/",
        views.EpisodeListView.as_view(),
        name="episode-list",
    ),
    path("episode/<int:pk>/edit/", views.edit_episode, name="edit-episode"),
    path(
        "episodes/update-status/",
        views.update_episode_statuses,
        name="edit-episode-statuses",
    ),
]
