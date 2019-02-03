from django import forms

from .models import Podcast, Episode


class BootstrapFormMixin(forms.Form):
    """A simple mix-in class to add bootstrap class to field widgets."""

    required_false = tuple()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        css_class = "form-control"
        for name, field in self.fields.items():
            if "class" in field.widget.attrs:
                field.widget.attrs["class"] += f" {css_class}"
            else:
                field.widget.attrs.update({"class": css_class})

            if name in self.required_false:
                field.required = False


class AddPodcastForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Podcast
        fields = ("url", "episode_number_pattern")
        labels = {"url": "RSS Feed URL"}

    required_false = ("episode_number_pattern",)


class EditPodcastForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Podcast
        exclude = ("id", "last_refreshed")


class EditEpisodeForm(forms.ModelForm, BootstrapFormMixin):
    class Meta:
        model = Episode
        fields = (
            "status",
            "title",
            "episode_number",
            "episode_part",
            "publication_timestamp",
            "audio_url",
            "_image_url",
            "description",
            "duration",
        )
        labels = {"audio_url": "Audio URL", "_image_url": "Image URL"}
        widgets = {"description": forms.Textarea(attrs={"cols": 80, "rows": 10})}

    required_false = (
        "title",
        "episode_number",
        "episode_part",
        "audio_url",
        "_image_url",
        "publication_timestamp",
        "duration",
    )

    def save(self, commit=True):
        if not self.cleaned_data["episode_number"]:
            self.instance.episode_number = None
        super().save(commit=commit)
