from django import forms

from .models import Podcast, Episode


class AddPodcastForm(forms.Form):
    url = forms.CharField(label="RSS Feed URL")


class EditPodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        exclude = ("id", "last_refreshed")


class EditEpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        exclude = ("id", "podcast")
