from dataclasses import dataclass
from enum import Enum, auto

from tablix import Field


@dataclass
class Terminal:
    """The renderer for pretty-printing the table into the terminal."""

    headers: list[Field]
    content: list[list[Field]]

    def lines(self) -> list[str]:
        """Return the string for each line of this table."""
        lines = []
        field_strings = _construct_field_strings(self.headers, self.content)
        for i, row in enumerate(field_strings):
            lines.append(_add_column_separators(row))

            if i == len(field_strings) - 1:
                continue

            separator_type = _SeparatorType.BOLD if i == 0 else _SeparatorType.NORMAL
            lines.append(_construct_separator_line(row, separator_type))

        return lines


def _construct_field_strings(headers: list[Field], content: list[list[Field]]) -> list[list[str]]:
    header_strings = [_stringify_format(field) for field in headers]
    content_strings = [[_stringify_format(field) for field in row] for row in content]

    column_widths = _determine_column_lengths(header_strings, content_strings)

    header_strings = [field.ljust(column_widths[i]) for i, field in enumerate(header_strings)]
    content_strings = [
        [field.ljust(column_widths[i]) for i, field in enumerate(row)] for row in content_strings
    ]

    return [header_strings, *content_strings]


def _determine_column_lengths(
    header_strings: list[str], content_strings: list[list[str]]
) -> list[int]:
    column_lengths = [len(field) for field in header_strings]

    for row in content_strings:
        for i, field in enumerate(row):
            column_lengths[i] = max(column_lengths[i], len(field))

    return column_lengths


def _stringify_format(field: Field) -> str:
    if field.format.bold:
        return f"**{field.value}**"
    if field.format.italic:
        return f"__{field.value}__"
    return field.value


def _add_column_separators(row: list[str]) -> str:
    return f"│ {' │ '.join(row)} │"


class _SeparatorType(Enum):
    NORMAL = auto()
    BOLD = auto()


def _construct_separator_line(row: list[str], separator_type: _SeparatorType) -> str:
    if separator_type == _SeparatorType.NORMAL:
        line = "├─"
        for i, field in enumerate(row):
            line += "─" * len(field)
            if i < len(row) - 1:
                line += "─┼─"

        line += "─┤"
        return line

    if separator_type == _SeparatorType.BOLD:
        line = "┝━"
        for i, field in enumerate(row):
            line += "━" * len(field)
            if i < len(row) - 1:
                line += "━┿━"

        line += "━┥"
        return line

    raise RuntimeError
