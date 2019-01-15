from django.urls import path

from podcast_log import views

urlpatterns = [
    path('', views.index, name='index'),
]
