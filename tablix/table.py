from __future__ import annotations

from dataclasses import dataclass, field

from tablix.format import Format


@dataclass
class Field:
    """A formatted field."""

    value: str
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
        content: list[list[str]],
        headers: list[str] | None = None,
    ) -> Table:
        """Construct a Table from a list."""
        if headers is None:
            headers = content.pop(0)

        processed_headers = [Field(value, Format()) for value in headers]
        processed_content = [[Field(value, Format()) for value in row] for row in content]
        return Table(processed_headers, processed_content)
