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
        if not self._table.rows:
            return []

        table = _add_field_padding(self._table)
        separators = _construct_separators(table)
        table = _blank_merged_fields(table)
        table = table.apply(_apply_format)

        lines = [separators[0]]
        for row, separator in zip(table.rows, separators[1:], strict=True):
            lines.append(_stringify_row(row))
            lines.append(separator)

        return lines


def _add_field_padding(table: _Rows) -> _Rows:
    new_columns = []
    for column in table.transpose:
        width = len(max(column.fields, key=lambda f: len(f.value)).value)
        new_fields = []
        for field in column.fields:
            new_val = field.value
            match field.format.align:
                case "auto":
                    new_val = field.value.ljust(width)
                case "left":
                    new_val = field.value.ljust(width)
                case "right":
                    new_val = field.value.rjust(width)
                case "center":
                    left_spaces = floor((width - len(field)) / 2)
                    right_spaces = ceil((width - len(field)) / 2)
                    new_val = " " * left_spaces + field.value + " " * right_spaces
            new_fields.append(_Field(new_val, field.format))
        new_columns.append(_Fields(new_fields))

    return _Rows(_Rows(new_columns).transpose)


def _blank_merged_fields(table: _Rows) -> _Rows:
    new_rows = []
    for r, row in enumerate(table.rows):
        if r == 0:
            new_rows.append(row)
            continue

        new_fields = []
        prev_row = table.rows[r - 1]
        for field, prev_field in zip(row.fields, prev_row.fields, strict=True):
            if (
                field.format.merge_same
                and prev_field.format.merge_same
                and field.value == prev_field.value
            ):
                new_fields.append(_Field(" " * len(field.value), field.format))
            else:
                new_fields.append(field)
        new_rows.append(_Fields(new_fields))

    return _Rows(new_rows)


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
    TOP = auto()
    BOTTOM = auto()
    NORMAL = auto()
    BOLD = auto()

    @property
    def fill_char(self) -> str:
        return "━" if self == _SeparatorType.BOLD else "─"

    def intersection(self, left_line: bool, right_line: bool) -> str:  # noqa: C901, PLR0911, PLR0912
        match self, left_line, right_line:
            case _SeparatorType.TOP, False, False:
                return " "
            case _SeparatorType.TOP, False, True:
                return "╭"
            case _SeparatorType.TOP, True, False:
                return "╮"
            case _SeparatorType.TOP, True, True:
                return "┬"

            case _SeparatorType.BOTTOM, False, False:
                return " "
            case _SeparatorType.BOTTOM, False, True:
                return "╰"
            case _SeparatorType.BOTTOM, True, False:
                return "╯"
            case _SeparatorType.BOTTOM, True, True:
                return "┴"

            case _SeparatorType.NORMAL, False, False:
                return "│"
            case _SeparatorType.NORMAL, False, True:
                return "├"
            case _SeparatorType.NORMAL, True, False:
                return "┤"
            case _SeparatorType.NORMAL, True, True:
                return "┼"

            case _SeparatorType.BOLD, False, False:
                return "│"
            case _SeparatorType.BOLD, False, True:
                return "┝"
            case _SeparatorType.BOLD, True, False:
                return "┥"
            case _SeparatorType.BOLD, True, True:
                return "┿"
        raise RuntimeError


def _construct_separators(table: _Rows) -> list[str]:
    if not table.rows:
        return []

    separators = [_construct_separator_line(None, table.rows[0], _SeparatorType.TOP)]

    for r, row in enumerate(table.rows):
        if table.is_last(row):
            separators.append(_construct_separator_line(row, None, _SeparatorType.BOTTOM))
            continue

        separator_type = _SeparatorType.BOLD if table.is_first(row) else _SeparatorType.NORMAL
        next_row = table.rows[r + 1]
        separators.append(_construct_separator_line(row, next_row, separator_type))

    return separators


def _construct_separator_line(
    row: _Fields | None, next_row: _Fields | None, separator_type: _SeparatorType
) -> str:
    reference_row = row if row is not None else next_row
    if reference_row is None:
        raise RuntimeError

    if separator_type in (_SeparatorType.TOP, _SeparatorType.BOTTOM, _SeparatorType.BOLD):
        merges = [False] * len(reference_row.fields)
    elif row is not None and next_row is not None:
        merges = [
            field.format.merge_same
            and next_field.format.merge_same
            and field.value == next_field.value
            for field, next_field in zip(row.fields, next_row.fields, strict=True)
        ]
    else:
        raise RuntimeError

    line = ""
    for i, field in enumerate(reference_row.fields):
        left_line = False if i == 0 else not merges[i - 1]
        right_line = not merges[i]

        line += separator_type.intersection(left_line, right_line)
        fill_char = separator_type.fill_char if not merges[i] else " "
        line += fill_char * (len(field) + 2)

    left_line = not merges[-1]
    right_line = False
    line += separator_type.intersection(left_line, right_line)

    return line
