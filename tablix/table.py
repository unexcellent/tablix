from __future__ import annotations

from dataclasses import dataclass

from tablix._core import _Field, _Fields, _Rows
from tablix.format import Format
from tablix.renderers.terminal import Terminal


@dataclass
class Table:
    """The class representation of a table."""

    _rows: _Rows

    @classmethod
    def from_list(
        cls,
        content: list[list[str | int | float | bool | tuple[str | int | float | bool, Format]]],
        column_formats: dict[int, Format] | None = None,
        row_formats: dict[int, Format] | None = None,
    ) -> Table:
        """Construct a Table from a list."""
        processed_content = [
            _Fields(
                [
                    _Field.from_value(
                        value, column_formats or {}, col, row_formats or {}, row_number
                    )
                    for col, value in enumerate(row)
                ]
            )
            for row_number, row in enumerate(content)
        ]
        return Table(_Rows(processed_content))

    def to_terminal(self) -> Terminal:
        """Convert this table to format that can be pretty-printed to the terminal."""
        return Terminal(self._rows)

    def __str__(self) -> str:
        return self.to_terminal().__str__()
