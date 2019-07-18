"""Table classes."""
from typing import List, Dict, Tuple, Any

from flask import url_for
from flask_table import Table, Col, OptCol, LinkCol
from flask_table.html import element

from podcast_log.models import STATUS_CHOICES, Episode


class ImageCol(Col):
    """A custom table column holding an image."""

    def td_format(self, content: str) -> str:
        """Format table cell content with proper HTML image tag."""
        return element("img", attrs={"src": content, "class": "img-episode-list"})


class SelectStatusCol(OptCol):
    """A custom table column to select table status and update the database."""

    def td_contents(self, item: Episode, attr_list: List[str]) -> str:
        """Construct an HTML form for updating the episode status in the database."""
        content = self.td_format(self.from_attr_list(item, attr_list))
        post_url = url_for("main.update_episode_status", episode_id=item.id)
        return f"""<form action="{post_url}" method="post">
            {content}
        </form>"""

    def td_format(self, content: str) -> str:
        """Format table cell content to contain a drop-down selector."""
        option_list = []
        for short, long in self.choices.items():
            selected = "selected" if content == short else ""
            option_list.append(f'<option value="{short}" {selected}>{long}</option>')
        options = "\n".join(option_list)
        return f"""<div class="form-group">
                        <select name="status" onchange="this.form.submit()">
                            {options}
                        </select>
                    </div>"""


class PodcastLinkCol(LinkCol):
    """Custom link column to show text as podcast title."""

    def text(self, item: Episode, attr_list: List[str]) -> str:
        """Format the cell contents to include a link to edit the episode."""
        return item.podcast.title


all_columns = {
    "image_url": ImageCol("Image"),
    "podcast": PodcastLinkCol(
        "Podcast", "main.podcast_detail", url_kwargs=dict(podcast_id="podcast_id")
    ),
    "episode_number": Col("Episode"),
    "title": Col("Title"),
    "publication_timestamp": Col("Publication Date"),
    "duration": Col("Duration"),
    "description": Col("Description"),
    "status": SelectStatusCol("Status", choices=STATUS_CHOICES),
    "edit": LinkCol(
        "Edit",
        "main.edit_episode",
        url_kwargs=dict(episode_id="id"),
        text_fallback="(Edit)",
    ),
}


class EpisodeTableBase(Table):
    """Base class for episode tables.

    Defines all available columns. Specific columns can be removed for specific usages by setting
    any column to None in a subclass.

    """

    allow_sort = False
    hide_cols: Tuple[str, ...] = tuple()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Override constructor to dynamically add columns to handle hidden columns."""
        super().__init__(*args, **kwargs)
        for col_name, col in all_columns.items():
            if col_name not in self.hide_cols:
                self.add_column(col_name, col)

    def sort_url(self, col_id: str, reverse: bool = False) -> str:
        """Provide a url for each column which will be called when the header is clicked to sort."""
        pass

    def get_tr_attrs(self, item: Episode) -> Dict[str, str]:
        """Assign attributes to the table row by assigning a CSS class."""
        return {"class": f"row-episode-{str(item.status).lower()}"}


class AllEpisodesTable(EpisodeTableBase):
    """A table showing all episodes.

    The description column is hidden to save space.

    """

    hide_cols = ("description",)


class PodcastEpisodesTable(EpisodeTableBase):
    """A table showing all episodes for a single podcast.

    The podcast column is hidden since the table only contains episodes from a single podcast.

    """

    hide_cols = ("podcast",)
