from __future__ import annotations

from collections.abc import Callable, Iterable
from copy import deepcopy
from dataclasses import dataclass, field

from tablix.format import Format


@dataclass
class _Field:
    value: str
    format: Format = field(default_factory=Format)

    @classmethod
    def from_value(
        cls,
        value: str | float | bool | tuple[str | int | float | bool, Format],
        column_formats: dict[int, Format],
        col: int,
        row_formats: dict[int, Format],
        row: int,
    ) -> _Field:
        """Construct a field from either just a value or a value-format combination."""
        if isinstance(value, tuple):
            return _Field(str(value[0]), _resolve_auto_align(value[0], value[1]))

        format_ = column_formats.get(col, Format.default())
        format_ = row_formats.get(row, format_)

        return _Field(str(value), _resolve_auto_align(value, format_))

    def apply(self, function: Callable) -> _Field:
        return function(self)

    def __len__(self) -> int:
        return len(self.value)


def _resolve_auto_align(value: str | float | bool, format_: Format) -> Format:
    if format_.align != "auto":
        return format_

    new_format = deepcopy(format_)
    if isinstance(value, str):
        new_format.align = "auto"
    if isinstance(value, int):
        new_format.align = "right"
    if isinstance(value, bool):
        new_format.align = "left"
    if isinstance(value, float):
        new_format.align = "left"

    return new_format


@dataclass
class _Fields:
    fields: list[_Field]

    def apply(self, function: Callable) -> _Fields:
        return _Fields([field.apply(function) for field in self.fields])


@dataclass
class _Rows:
    rows: list[_Fields]

    @property
    def header_row(self) -> _Fields:
        return self.rows[0]

    @property
    def content_rows(self) -> list[_Fields]:
        return self.rows[1:]

    @property
    def transpose(self) -> list[_Fields]:
        return [
            _Fields(list(column_data))
            for column_data in zip(*(row.fields for row in self.rows), strict=True)
        ]

    def apply(self, function: Callable) -> _Rows:
        return _Rows([row.apply(function) for row in self.rows])

    def is_first(self, row: _Fields) -> bool:
        return row == self.rows[0]

    def is_last(self, row: _Fields) -> bool:
        return row == self.rows[-1]

    def enumerate(self) -> Iterable[tuple[int, int, _Field]]:
        for r, row in enumerate(self.rows):
            for c, field_ in enumerate(row.fields):
                yield r, c, field_

    def get(self, row: int, column: int) -> _Field | None:
        try:
            return self.rows[row].fields[column]
        except IndexError:
            return None
