from typing import Generator

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, Field
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.validators import InputRequired

from podcast_log.models import db, Podcast, Episode


class ModelFormBase(FlaskForm):
    """Base class adding easy access to a list of fields for template."""

    @property
    def fields(self) -> Generator[Field, None, None]:
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

EditEpisodeForm = model_form(
    Episode,
    db_session=db,
    base_class=ModelFormBase,
    only=[
        "title",
        "publication_timestamp",
        "episode_number",
        "episode_part",
        "description",
        "audio_url",
        "status",
        "needs_review",
    ],
)
