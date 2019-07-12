"""Table classes."""
from typing import List, Dict

from flask import url_for
from flask_table import Table, Col, OptCol

from podcast_log.models import STATUS_CHOICES, Episode


def get_episode_class(record: Episode) -> str:
    """Return a CSS class string name for the table rows, based on episode status."""
    class_str = record.get_status_display().lower()
    return f"row-episode-{'-'.join(class_str.split())}"


class ImageCol(Col):
    """A custom table column holding an image."""

    def td_format(self, content: str) -> str:
        """Format table cell content with proper HTML image tag."""
        return f'<img src="{content}" class="img-episode-list">'


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


class EditCol(Col):
    """A custom table column containing a hyperlink to edit the episode."""

    def td_contents(self, item: Episode, attr_list: List[str]) -> str:
        """Format the cell contents to include a link to edit the episode."""
        link_url = url_for("main.edit_episode", episode_id=item.id)
        content = f"""<a href="{link_url}">(Edit)</a>"""
        return self.td_format(content)

    def td_format(self, content: str) -> str:
        """Don't escape the HTML content."""
        return content


class EpisodeTableBase(Table):
    """Base class for episode tables.

    Defines all available columns. Specific columns can be removed for specific usages by setting
    any column to None in a subclass.

    """

    image_url = ImageCol("Image")
    podcast = Col("Podcast")
    episode_number = Col("Episode")
    title = Col("Title")
    publication_timestamp = Col("Publication Date")
    duration = Col("Duration")
    description = Col("Description")
    status = SelectStatusCol("Status", choices=STATUS_CHOICES)
    edit = EditCol("Edit")

    allow_sort = False

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

    description = None


class PodcastEpisodesTable(EpisodeTableBase):
    """A table showing all episodes for a single podcast.

    The podcast column is hidden since the table only contains episodes from a single podcast.

    """

    podcast = None
