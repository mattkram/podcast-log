from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.validators import InputRequired

from podcast_log.models import db, Podcast


class ModelFormBase(FlaskForm):
    """Base class adding easy access to a list of fields for template."""

    @property
    def fields(self):
        for name, field in self._fields.items():
            if name != "csrf_token":
                yield field


class AddPodcastForm(FlaskForm):
    url = StringField(label="URL", validators=[InputRequired()])
    episode_number_pattern = StringField("Episode Number Pattern")
    submit = SubmitField()


EditPodcastForm = model_form(
    Podcast,
    db_session=db,
    base_class=ModelFormBase,
    only=["title", "url", "summary", "episode_number_pattern"],
)

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
