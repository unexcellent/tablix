from dataclasses import dataclass

from tablix import Field


@dataclass
class Markdown:
    """The renderer for the markdown table format."""

    headers: list[Field]
    content: list[list[Field]]

    def lines(self) -> list[str]:
        """Return the string for each line of this table."""
        column_lengths = self._determine_column_lengths()

        header_row = [field.value.ljust(column_lengths[i]) for i, field in enumerate(self.headers)]
        separator_row = ["-" * length for length in column_lengths]
        body_rows = [
            [field.value.ljust(column_lengths[i]) for i, field in enumerate(row)]
            for row in self.content
        ]

        all_rows = [header_row, separator_row, *body_rows]
        return [f"| {' | '.join(row)} |" for row in all_rows]

    def _determine_column_lengths(self) -> list[int]:
        column_lengths = [len(col.value) for col in self.headers]

        for row in self.content:
            for col, field in enumerate(row):
                column_lengths[col] = max(column_lengths[col], len(field.value))

        return column_lengths
