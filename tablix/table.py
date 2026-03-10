from __future__ import annotations

from dataclasses import dataclass, field

from tablix.format import Format


@dataclass
class Field:
    """A formatted field."""

    value: str
    format: Format = field(default_factory=Format)

    @classmethod
    def from_value(cls, value: str | tuple[str, Format]) -> Field:
        """Construct a field from either just a value or a value-format combination."""
        if isinstance(value, tuple):
            return Field(value[0], value[1])
        return Field(value, Format.default())


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
    ) -> Table:
        """Construct a Table from a list."""
        if headers is None:
            headers = content.pop(0)

        processed_headers = [Field.from_value(value) for value in headers]
        processed_content = [[Field.from_value(value) for value in row] for row in content]
        return Table(processed_headers, processed_content)
