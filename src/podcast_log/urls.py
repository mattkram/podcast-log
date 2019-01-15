from django.urls import path

from src.podcast_log import views

urlpatterns = [path("", views.index, name="index")]
