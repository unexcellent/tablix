from dataclasses import dataclass

from tablix import Field


@dataclass
class Markdown:
    """The renderer for the markdown table format."""

    headers: list[Field]
    content: list[list[Field]]

    def lines(self) -> list[str]:
        """Return the string for each line of this table."""
        all_rows = _construct_field_strings(self.headers, self.content)
        return [f"| {' | '.join(row)} |" for row in all_rows]


def _construct_field_strings(headers: list[Field], content: list[list[Field]]) -> list[list[str]]:
    header_strings = [_stringify_format(field) for field in headers]
    content_strings = [[_stringify_format(field) for field in row] for row in content]

    column_widths = _determine_column_lengths(header_strings, content_strings)

    header_strings = [field.ljust(column_widths[i]) for i, field in enumerate(header_strings)]
    content_strings = [
        [field.ljust(column_widths[i]) for i, field in enumerate(row)] for row in content_strings
    ]
    separator_strings = ["-" * length for length in column_widths]

    return [header_strings, separator_strings, *content_strings]


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
