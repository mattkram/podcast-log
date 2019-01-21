from django.urls import path

from . import views

urlpatterns = [
    path("", views.PodcastListView.as_view(), name="index"),
    path("episodes/", views.EpisodeListView.as_view(), name="episodes"),
    path("<int:pk>/", views.PodcastDetailView.as_view(), name="podcast"),
    path("<int:pk>/update/", views.update_podcast, name="update-podcast"),
    path("<int:pk>/edit/", views.edit_podcast, name="edit-podcast"),
    path("update/", views.update_podcasts, name="update_all"),
    path("add/", views.add_podcast, name="add-podcast"),
]
