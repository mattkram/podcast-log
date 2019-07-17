"""Simple pagination utilities.

<ul class="pagination">
    <li class="page-item"><a class="page-link" href="#">Previous</a></li>
    <li class="page-item"><a class="page-link" href="#">1</a></li>
    <li class="page-item"><a class="page-link" href="#">2</a></li>
    <li class="page-item"><a class="page-link" href="#">3</a></li>
    <li class="page-item"><a class="page-link" href="#">...</a></li>
    <li class="page-item"><a class="page-link" href="#">98</a></li>
    <li class="page-item"><a class="page-link" href="#">99</a></li>
    <li class="page-item"><a class="page-link" href="#">100</a></li>
    <li class="page-item"><a class="page-link" href="#">Next</a></li>
</ul>
"""
from typing import Any, List

from flask_sqlalchemy import BaseQuery
from sqlalchemy import Column


class Paginator:
    """A simple paginator.

    Also contains methods for obtaining items from a database query and generating the navigation
    bar.

    """

    def __init__(
        self,
        query: BaseQuery,
        *,
        sort_column: Column = None,
        reverse_sort: bool = False,
        page: int = 1,
        items_per_page: int = 20
    ):
        self.query = query
        self.page = page
        self.items_per_page = items_per_page
        self.sort_column = sort_column
        self.reverse_sort = reverse_sort

    @property
    def items(self) -> List[Any]:
        """Retrieve a list of items for a specific page, optionally sorted by a model column."""
        items = self.query
        if self.sort_column:
            if self.reverse_sort:
                o = self.sort_column.desc()
            else:
                o = self.sort_column.asc()
            items = items.order_by(o)

        return items.paginate(self.page, self.items_per_page, False).items
