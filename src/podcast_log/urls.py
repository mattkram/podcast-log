from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="podcasts"),
    path("episodes/", views.IndexView.as_view(), name="episodes"),
    path("<int:pk>/", views.DetailView.as_view(), name="podcast"),
]
