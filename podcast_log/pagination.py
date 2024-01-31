"""Simple pagination utilities."""

from __future__ import annotations

from typing import Any, Optional

from flask import request
from flask_sqlalchemy import BaseQuery
from sqlalchemy import Column
from werkzeug.urls import url_encode


class Paginator:
    """A simple paginator.

    Also contains methods for obtaining items from a database query and generating the navigation
    bar.

    """

    def __init__(
        self,
        query: BaseQuery,
        *,
        sort_column: Optional[Column] = None,
        reverse_sort: bool = False,
        page: int = 1,
        items_per_page: int = 20,
    ):
        self.query = query
        self.page = page
        self.items_per_page = items_per_page
        self.sort_column = sort_column
        self.reverse_sort = reverse_sort

    @property
    def items(self) -> list[Any]:
        """Retrieve a list of items for a specific page, optionally sorted by a model column."""
        items = self.query
        if self.sort_column:
            if self.reverse_sort:
                o = self.sort_column.desc()
            else:
                o = self.sort_column.asc()
            items = items.order_by(o)

        return items.paginate(
            page=self.page, per_page=self.items_per_page, count=False
        ).items

    @property
    def pages(self) -> list[dict[str, str]]:
        """Construct pagination buttons."""
        total_pages = len(self.query.all()) // self.items_per_page + 1
        previous_page = max(self.page - 1, 1)
        next_page = min(self.page + 1, total_pages)

        def make_url(page_num: int) -> str:
            args = request.args.copy()
            args["page"] = str(page_num)
            return f"{request.path}?{url_encode(args)}"

        page_buttons = [{"url": make_url(previous_page), "text": "Previous"}]
        for page in range(1, total_pages + 1):
            page_buttons.append({"url": make_url(page), "text": f"{page}"})
        page_buttons.append({"url": make_url(next_page), "text": "Next"})

        page_buttons[self.page]["status"] = "active"
        if self.page == 1:
            page_buttons[0]["status"] = "disabled"
        if self.page == total_pages:
            page_buttons[-1]["status"] = "disabled"

        return page_buttons
