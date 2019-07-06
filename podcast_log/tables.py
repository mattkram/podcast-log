from typing import List, Dict

from flask import url_for
from flask_table import Table, Col, OptCol

from podcast_log.models import STATUS_CHOICES, Episode


def get_episode_class(record: Episode) -> str:
    """Return a CSS class string name for the table rows, based on episode status."""
    class_str = record.get_status_display().lower()
    return f"row-episode-{'-'.join(class_str.split())}"


class ImageCol(Col):
    def td_format(self, content: str) -> str:
        return f'<img src="{content}" class="img-episode-list">'


class SelectStatusCol(OptCol):
    def td_contents(self, item: Episode, attr_list: List[str]) -> str:
        content = self.td_format(self.from_attr_list(item, attr_list))
        return f"""<form action="{url_for("main.update_episode_status", episode_id=item.id)}" method="post">
            {content}
        </form>"""

    def td_format(self, content) -> str:
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
    def td_contents(self, item: Episode, attr_list: List[str]) -> str:
        content = f"""<a href="{url_for("main.edit_episode", episode_id=item.id)}">(Edit)</a>"""
        return self.td_format(content)

    def td_format(self, content):
        return content


class EpisodeTableBase(Table):
    image_url = ImageCol("Image")
    podcast = Col("Podcast")
    episode_number = Col("Episode")
    title = Col("Title")
    publication_timestamp = Col("Publication Date")
    duration = Col("Duration")
    description = Col("Description")
    status = SelectStatusCol("Status", choices=STATUS_CHOICES)
    edit = EditCol("Edit")

    def get_tr_attrs(self, item: Episode) -> Dict[str, str]:
        return {"class": f"row-episode-{str(item.status).lower()}"}


class AllEpisodesTable(EpisodeTableBase):
    description = None


class PodcastEpisodesTable(EpisodeTableBase):
    podcast = None
