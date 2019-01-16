from django.urls import path

from . import views

urlpatterns = [
    path("", views.PodcastListView.as_view(), name="podcasts"),
    path("episodes/", views.EpisodeListView.as_view(), name="episodes"),
    path("<int:pk>/", views.PodcastDetailView.as_view(), name="podcast"),
]
