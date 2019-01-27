from django import forms

from .models import Podcast, Episode


class AddPodcastForm(forms.Form):
    url = forms.CharField(label="RSS Feed URL")


class EditPodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        exclude = ("id", "last_refreshed")


class EditEpisodeForm(forms.ModelForm):

    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=False
    )
    episode_number = forms.CharField(
        widget=forms.NumberInput(attrs={"class": "form-control"}), required=False
    )
    episode_part = forms.CharField(
        widget=forms.NumberInput(attrs={"class": "form-control"}), required=False
    )
    audio_url = forms.URLField(
        required=False, widget=forms.URLInput(attrs={"class": "form-control"})
    )
    image_url = forms.URLField(
        required=False, widget=forms.URLInput(attrs={"class": "form-control"})
    )
    publication_timestamp = forms.DateTimeField(
        required=False, widget=forms.DateTimeInput(attrs={"class": "form-control"})
    )
    duration = forms.DurationField(
        required=False, widget=forms.TimeInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Episode
        fields = (
            "status",
            "title",
            "episode_number",
            "episode_part",
            "publication_timestamp",
            "audio_url",
            "image_url",
            "description",
            "duration",
        )

        widgets = {
            "description": forms.Textarea(
                attrs={"class": "form-control", "cols": 80, "rows": 10}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        if not self.cleaned_data["episode_number"]:
            self.instance.episode_number = None
        super().save(commit=commit)
