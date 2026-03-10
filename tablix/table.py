from __future__ import annotations

from dataclasses import dataclass

from tablix.field import Field
from tablix.format import Format


@dataclass
class Table:
    """The class representation of a table."""

    headers: list[Field]
    """The headers of each column."""

    content: list[list[Field]]
    """The table content.

    The first index is the rows and the second the columns."""

    @classmethod
    def from_list(
        cls,
        content: list[list[str | tuple[str, Format]]],
        headers: list[str | tuple[str, Format]] | None = None,
        column_formats: dict[int, Format] | None = None,
        row_formats: dict[int, Format] | None = None,
    ) -> Table:
        """Construct a Table from a list."""
        if headers is None:
            headers = content.pop(0)

        if column_formats is None:
            column_formats = {}

        if row_formats is None:
            row_formats = {}

        processed_headers = [
            Field.from_value(value, column_formats, col, row_formats, 0)
            for col, value in enumerate(headers)
        ]
        processed_content = [
            [
                Field.from_value(value, column_formats, col, row_formats, row_number + 1)
                for col, value in enumerate(row)
            ]
            for row_number, row in enumerate(content)
        ]
        return Table(processed_headers, processed_content)
