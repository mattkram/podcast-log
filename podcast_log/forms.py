from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class AddPodcastForm(FlaskForm):
    url = StringField(label="URL", validators=[InputRequired()])
    episode_number_pattern = StringField("Episode Number Pattern")
    submit = SubmitField()


# class EditPodcastForm(forms.ModelForm, BootstrapFormMixin):
#     class Meta:
#         model = Podcast
#         exclude = ("id", "last_refreshed")
#
#
# class EditEpisodeForm(forms.ModelForm, BootstrapFormMixin):
#     class Meta:
#         model = Episode
#         fields = (
#             "status",
#             "title",
#             "episode_number",
#             "episode_part",
#             "publication_timestamp",
#             "audio_url",
#             "_image_url",
#             "description",
#             "duration",
#         )
#         labels = {"audio_url": "Audio URL", "_image_url": "Image URL"}
#         widgets = {"description": forms.Textarea(attrs={"cols": 80, "rows": 10})}
#
#     required_false = (
#         "title",
#         "episode_number",
#         "episode_part",
#         "audio_url",
#         "_image_url",
#         "publication_timestamp",
#         "duration",
#     )
#
#     def save(self, commit=True):
#         if not self.cleaned_data["episode_number"]:
#             self.instance.episode_number = None
#         super().save(commit=commit)
