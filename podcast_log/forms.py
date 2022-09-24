"""Forms for interacting with database models."""
from __future__ import annotations

from collections.abc import Generator

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import Field, FileField, StringField, SubmitField
from wtforms.validators import InputRequired
from wtforms_sqlalchemy.orm import model_form

from podcast_log.models import Episode, Podcast, db


class ModelFormBase(FlaskForm):
    """Base class adding easy access to a list of fields for template."""

    @property
    def fields(self) -> Generator[Field, None, None]:
        """Iterate through the form fields, ignoring the csrf_token."""
        for name, field in self._fields.items():
            if name != "csrf_token":
                yield field


class AddPodcastForm(FlaskForm):
    """A form used for adding a new podcast."""

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


class FileUploadForm(FlaskForm):
    """A simple form to upload a file."""

    file = FileField(label="Choose file:", validators=[FileRequired()])
    submit = SubmitField()
