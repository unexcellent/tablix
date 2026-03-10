from __future__ import annotations

from dataclasses import dataclass, field

from tablix.format import Format


@dataclass
class Field:
    """A formatted field."""

    value: str
    format: Format = field(default_factory=Format)

    @classmethod
    def from_value(
        cls, value: str | tuple[str, Format], column_formats: list[Format], col: int
    ) -> Field:
        """Construct a field from either just a value or a value-format combination."""
        if isinstance(value, tuple):
            return Field(value[0], value[1])

        format_ = column_formats[col] if col < len(column_formats) else Format.default()

        return Field(value, format_)


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
        column_formats: list[Format] | None = None,
    ) -> Table:
        """Construct a Table from a list."""
        if headers is None:
            headers = content.pop(0)

        if column_formats is None:
            column_formats = []

        processed_headers = [
            Field.from_value(value, column_formats, col) for col, value in enumerate(headers)
        ]
        processed_content = [
            [Field.from_value(value, column_formats, col) for col, value in enumerate(row)]
            for row in content
        ]
        return Table(processed_headers, processed_content)
