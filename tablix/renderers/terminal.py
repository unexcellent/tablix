from dataclasses import dataclass
from enum import Enum, auto

from tablix import Field
from tablix.renderers._renderer import _Renderer


@dataclass
class Terminal(_Renderer):
    """The renderer for pretty-printing the table into the terminal."""

    headers: list[Field]
    content: list[list[Field]]

    def lines(self) -> list[str]:
        """Return the string for each line of this table."""
        lines = []
        fields = _construct_field_strings(self.headers, self.content)
        for i, row in enumerate(fields):
            lines.append(_add_column_separators([_stringify_format(field) for field in row]))

            if i == len(fields) - 1:
                continue

            separator_type = _SeparatorType.BOLD if i == 0 else _SeparatorType.NORMAL
            lines.append(_construct_separator_line([field.value for field in row], separator_type))

        return lines


def _construct_field_strings(headers: list[Field], content: list[list[Field]]) -> list[list[Field]]:
    column_widths = _determine_column_lengths(headers, content)

    for i, field in enumerate(headers):
        headers[i].value = field.value.ljust(column_widths[i])

    for r, row in enumerate(content):
        for c, field in enumerate(row):
            content[r][c].value = field.value.ljust(column_widths[c])

    return [headers, *content]


def _determine_column_lengths(
    header_strings: list[Field], content_strings: list[list[Field]]
) -> list[int]:
    column_lengths = [len(field.value) for field in header_strings]

    for row in content_strings:
        for i, field in enumerate(row):
            column_lengths[i] = max(column_lengths[i], len(field.value))

    return column_lengths


def _stringify_format(field: Field) -> str:
    if field.format.bold:
        return f"\033[1m{field.value}\033[0m"
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
