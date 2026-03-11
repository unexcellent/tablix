from dataclasses import dataclass
from enum import Enum, auto
from math import ceil, floor

from tablix._core import _Field, _Fields, _Rows
from tablix.renderers._renderer import _Renderer


@dataclass
class Terminal(_Renderer):
    """The renderer for pretty-printing the table into the terminal."""

    _table: _Rows

    def lines(self) -> list[str]:
        """Return the string for each line of this table."""
        table = _add_field_padding(self._table)
        separators = _construct_separators(table)
        table = table.apply(_apply_format)
        lines = []
        for row, separator in zip(table.rows, separators, strict=True):
            lines.append(_stringify_row(row))
            lines.append(separator)

        return lines[:-1]


def _add_field_padding(table: _Rows) -> _Rows:
    columns = table.transpose
    for column in columns:
        width = len(max(column.fields, key=lambda field: len(field.value)).value)
        for field in column.fields:
            match field.format.align:
                case "left":
                    field.value = field.value.ljust(width)
                case "right":
                    field.value = field.value.rjust(width)
                case "center":
                    left_spaces = floor((width - len(field)) / 2)
                    right_spaces = ceil((width - len(field)) / 2)
                    field.value = " " * left_spaces + field.value + " " * right_spaces

    return _Rows(_Rows(columns).transpose)


def _apply_format(field: _Field) -> _Field:
    if field.format.bold:
        return _Field(f"\033[1m{field.value}\033[0m", field.format)
    return _Field(field.value, field.format)


def _stringify_row(row: _Fields) -> str:
    string = "│"
    for field in row.fields:
        string += f" {field.value} │"
    return string


class _SeparatorType(Enum):
    NORMAL = auto()
    BOLD = auto()


def _construct_separators(table: _Rows) -> list[str]:
    separators = []
    for row in table.rows:
        if table.is_last(row):
            separators.append("")
            continue

        separator_type = _SeparatorType.BOLD if table.is_first(row) else _SeparatorType.NORMAL
        separators.append(_construct_separator_line(row, separator_type))

    return separators


def _construct_separator_line(row: _Fields, separator_type: _SeparatorType) -> str:
    if separator_type == _SeparatorType.NORMAL:
        line = "├─"
        for i, field in enumerate(row.fields):
            line += "─" * len(field)
            if i < len(row.fields) - 1:
                line += "─┼─"

        line += "─┤"
        return line

    if separator_type == _SeparatorType.BOLD:
        line = "┝━"
        for i, field in enumerate(row.fields):
            line += "━" * len(field)
            if i < len(row.fields) - 1:
                line += "━┿━"

        line += "━┥"
        return line

    raise RuntimeError
