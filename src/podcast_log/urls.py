from django.urls import path

from . import views

urlpatterns = [
    path("", views.PodcastListView.as_view(), name="index"),
    path("episodes/", views.EpisodeListView.as_view(), name="episodes"),
    path("<int:pk>/", views.PodcastDetailView.as_view(), name="podcast"),
    path("update/", views.update_podcasts, name="update_all"),
    path("update/<int:pk>/", views.update_podcast, name="update-podcast"),
    path("add/", views.add_podcast, name="add-podcast"),
]
