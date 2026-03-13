from __future__ import annotations

from dataclasses import dataclass
from math import ceil, floor

from tablix._core import _Field, _Fields, _Rows
from tablix.renderers._renderer import _Renderer


@dataclass
class Markdown(_Renderer):
    """The renderer for formatting the table as Markdown."""

    _table: _Rows

    def lines(self) -> list[str]:
        """Return the string for each line of this table."""
        if not self._table.rows:
            return []

        table = _apply_markdown_formatting(self._table)
        widths = _calculate_column_widths(table)

        table = _blank_merged_fields(table)
        table = _add_field_padding(table, widths)

        lines = []
        for r, row in enumerate(table.rows):
            lines.append(_stringify_row(row))
            if r == 0:
                lines.append(_construct_separator(self._table, widths))

        return lines


def _apply_markdown_formatting(table: _Rows) -> _Rows:
    def apply_format(field: _Field) -> _Field:
        if field.format.bold:
            return _Field(f"**{field.value}**", field.format)
        if field.format.italic:
            return _Field(f"*{field.value}*", field.format)
        return _Field(field.value, field.format)

    return table.apply(apply_format)


def _calculate_column_widths(table: _Rows) -> list[int]:
    return [max(len(field.value) for field in column.fields) for column in table.transpose]


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
                new_fields.append(_Field("", field.format))
            else:
                new_fields.append(field)
        new_rows.append(_Fields(new_fields))

    return _Rows(new_rows)


def _add_field_padding(table: _Rows, widths: list[int]) -> _Rows:
    new_columns = []
    for c, column in enumerate(table.transpose):
        width = widths[c]
        new_fields = []
        for field in column.fields:
            new_val = field.value
            match field.format.align:
                case "auto" | "left":
                    new_val = field.value.ljust(width)
                case "right":
                    new_val = field.value.rjust(width)
                case "center":
                    left_spaces = floor((width - len(field.value)) / 2)
                    right_spaces = ceil((width - len(field.value)) / 2)
                    new_val = " " * left_spaces + field.value + " " * right_spaces
            new_fields.append(_Field(new_val, field.format))
        new_columns.append(_Fields(new_fields))

    return _Rows(_Rows(new_columns).transpose)


def _stringify_row(row: _Fields) -> str:
    return "| " + " | ".join(field.value for field in row.fields) + " |"


def _construct_separator(original_table: _Rows, widths: list[int]) -> str:
    parts = []
    for c, column in enumerate(original_table.transpose):
        width = widths[c]
        aligns = {"left" if f.format.align == "auto" else f.format.align for f in column.fields}

        # Deduce column alignment for the separator line. Fallback to 'left' if inconsistent.
        col_align = aligns.pop() if len(aligns) == 1 else "left"

        if col_align == "right":
            parts.append("-" * (width - 1) + ":")
        elif col_align == "center":
            parts.append(":" + "-" * (width - 2) + ":")
        else:
            parts.append(":" + "-" * (width - 1))

    return "| " + " | ".join(parts) + " |"
