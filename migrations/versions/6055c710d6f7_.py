"""empty message

Revision ID: 6055c710d6f7
Revises:
Create Date: 2019-05-31 21:49:49.079125

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6055c710d6f7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "podcast",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=True),
        sa.Column("url", sa.String(length=500), nullable=True),
        sa.Column("image_url", sa.String(length=500), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("last_refreshed", sa.DateTime(), nullable=True),
        sa.Column("refresh_interval", sa.Interval(), nullable=True),
        sa.Column("episode_number_pattern", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "episode",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("podcast_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=True),
        sa.Column("publication_timestamp", sa.DateTime(), nullable=True),
        sa.Column("audio_url", sa.String(length=500), nullable=True),
        sa.Column("_image_url", sa.String(length=500), nullable=True),
        sa.Column("description", sa.String(length=5000), nullable=True),
        sa.Column("duration", sa.Interval(), nullable=True),
        sa.Column("episode_number", sa.Integer(), nullable=True),
        sa.Column("episode_part", sa.Integer(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "LISTENED", "IGNORED", "SKIPPED", "IN_PROGRESS", "QUEUED", name="status"
            ),
            nullable=True,
        ),
        sa.Column("needs_review", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["podcast_id"],
            ["podcast.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("episode")
    op.drop_table("podcast")
