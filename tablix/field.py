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
        cls,
        value: str | tuple[str, Format],
        column_formats: dict[int, Format],
        col: int,
        row_formats: dict[int, Format],
        row: int,
    ) -> Field:
        """Construct a field from either just a value or a value-format combination."""
        if isinstance(value, tuple):
            return Field(value[0], value[1])

        format_ = column_formats.get(col, Format.default())
        format_ = row_formats.get(row, format_)

        return Field(value, format_)
