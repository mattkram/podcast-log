from django import forms
from django.forms import (
    TextInput,
    DateTimeInput,
    Textarea,
    URLInput,
    TimeInput,
    Select,
    NumberInput,
    URLField,
    CharField,
)

from .models import Podcast, Episode


class AddPodcastForm(forms.Form):
    url = forms.CharField(label="RSS Feed URL")


class EditPodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        exclude = ("id", "last_refreshed")


class EditEpisodeForm(forms.ModelForm):

    title = CharField(widget=TextInput(attrs={"class": "form-control"}), required=False)
    episode_number = CharField(
        widget=NumberInput(attrs={"class": "form-control"}), required=False
    )
    audio_url = URLField(
        required=False, widget=URLInput(attrs={"class": "form-control"})
    )
    image_url = URLField(
        required=False, widget=URLInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Episode
        fields = (
            "status",
            "title",
            "episode_number",
            "publication_timestamp",
            "audio_url",
            "image_url",
            "description",
            "duration",
        )

        widgets = {
            "publication_timestamp": DateTimeInput(attrs={"class": "form-control"}),
            "description": Textarea(
                attrs={"class": "form-control", "cols": 80, "rows": 10}
            ),
            "duration": TimeInput(attrs={"class": "form-control"}),
            "status": Select(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        if not self.cleaned_data["episode_number"]:
            self.instance.episode_number = None
        super().save(commit=commit)
