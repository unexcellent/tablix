from __future__ import annotations

from dataclasses import dataclass, field

from tablix.format import Format


@dataclass
class Field:
    """A formatted field."""

    value: str | int | float | bool | None = None
    format: Format = field(default_factory=Format)


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
        content: list[list[str | int | float | bool | None]],
        headers: list[str],
    ) -> Table:
        """Construct a Table from a list."""
        processed_headers = [Field(value, Format()) for value in headers]
        processed_content = [[Field(value, Format()) for value in row] for row in content]
        return Table(processed_headers, processed_content)
