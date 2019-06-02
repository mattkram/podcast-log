from marshmallow import Schema, fields


class PodcastSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    url = fields.Url()
    image_url = fields.Url()
    summary = fields.String()
    last_refreshed = fields.DateTime()
    refresh_interval = fields.TimeDelta()
    episode_number_pattern = fields.String()
    needs_update = fields.Boolean()
    statistics = fields.Nested("PodcastStatisticsSchema")
    episodes = fields.Nested("EpisodeSchema", many=True, exclude=("podcast",))


class PodcastStatisticsSchema(Schema):
    num_episodes = fields.Integer()
    num_listened = fields.Integer()
    num_ignored = fields.Integer()
    num_skipped = fields.Integer()
    num_in_progress = fields.Integer()
    num_queued = fields.Integer()
    progress = fields.String()
    time_listened = fields.TimeDelta()


class EpisodeSchema(Schema):
    id = fields.Integer()
    podcast = fields.Nested("PodcastSchema", only=("id", "title"))
    title = fields.String()
    publication_timestamp = fields.DateTime()
    audio_url = fields.Url()
    image_url = fields.Url()
    description = fields.String()
    duration = fields.TimeDelta()
    episode_number = fields.Integer()
    episode_part = fields.Integer()
    status = fields.String()
    needs_review = fields.Boolean()
