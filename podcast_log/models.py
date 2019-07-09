import enum
from datetime import timedelta, datetime
from typing import Any, Optional

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, Model


class ModelBase(Model):
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()


db: Any = SQLAlchemy(model_class=ModelBase)
migrate = Migrate()


class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    url = db.Column(db.String(500))
    image_url = db.Column(db.String(500))
    summary = db.Column(db.Text)
    last_refreshed = db.Column(db.DateTime, default=datetime(1, 1, 1))
    refresh_interval = db.Column(db.Interval, default=timedelta(hours=1))
    episode_number_pattern = db.Column(db.String(50), nullable=True)

    episodes = db.relationship(
        "Episode", backref="podcast", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return self.title

    @property
    def statistics(self) -> "PodcastStatistics":
        return PodcastStatistics(self)

    @property
    def needs_update(self) -> bool:
        update_after = self.last_refreshed + self.refresh_interval
        return update_after <= datetime.now()


class PodcastStatistics:
    def __init__(self, podcast: Podcast):
        self.podcast = podcast

    @property
    def num_episodes(self) -> int:
        return len(list(self.podcast.episodes))

    def __getattr__(self, name: str) -> Any:
        if name.startswith("num_"):
            try:
                status = getattr(Status, name.replace("num_", "").upper())
            except AttributeError:
                raise AttributeError(
                    f"Attribute {name} cannot be accessed, no associated episode status"
                )
            return len(list(self.podcast.episodes.filter_by(status=status)))
        return super().__getattribute__(name)

    @property
    def progress(self) -> str:
        num_to_listen = self.num_episodes - self.num_ignored
        pct_listened = (
            100 * self.num_listened / num_to_listen if num_to_listen > 0 else 0.0
        )
        return f"{self.num_listened} / {num_to_listen} ({pct_listened:0.1f}%)"

    @property
    def time_listened(self) -> timedelta:
        time_listened = timedelta(seconds=0)
        for e in self.podcast.episodes.filter(status=Episode.LISTENED):
            if e.duration is not None:
                time_listened += e.duration
        return time_listened


class Status(enum.Enum):
    LISTENED = "L"
    IGNORED = "I"
    SKIPPED = "S"
    IN_PROGRESS = "P"
    QUEUED = "Q"

    def __str__(self) -> str:
        return STATUS_CHOICES[self]


STATUS_CHOICES = {
    Status.QUEUED: "Queued",
    Status.LISTENED: "Listened",
    Status.IN_PROGRESS: "In Progress",
    Status.SKIPPED: "Skipped",
    Status.IGNORED: "Ignored",
}


class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    podcast_id = db.Column(db.Integer, db.ForeignKey("podcast.id"))

    title = db.Column(db.String(200))
    publication_timestamp = db.Column(db.DateTime, nullable=True)
    audio_url = db.Column(db.String(500), nullable=True)
    _image_url = db.Column(db.String(500), nullable=True)
    description = db.Column(db.String(5000), nullable=True)
    duration = db.Column(db.Interval, nullable=True)
    episode_number = db.Column(db.Integer, nullable=True)
    episode_part = db.Column(db.Integer, default=1)

    status = db.Column(db.Enum(Status), default=Status.QUEUED)

    needs_review = db.Column(db.Boolean, default=False)

    # class Meta:
    #     unique_together = ("podcast", "episode_number", "episode_part")

    def __str__(self) -> str:
        return f"Episode {self.episode_number}"

    @property
    def publication_date(self) -> Optional[datetime]:
        t = self.publication_timestamp
        if t is None:
            return None
        return datetime(year=t.year, month=t.month, day=t.day)

    @property
    def image_url(self) -> str:
        """str: Read-only property returning episode image URL, defaulting to podcast image if episode image missing."""
        if not self._image_url:
            return self.podcast.image_url
        return self._image_url

    @image_url.setter
    def image_url(self, value: str) -> None:
        self._image_url = value


def init_app(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)


def create_db(app: Flask) -> None:
    with app.app_context():
        db.create_all()
