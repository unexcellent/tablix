from __future__ import annotations

from dataclasses import dataclass

from tablix._core import _Field, _Fields, _Rows
from tablix.renderers._renderer import _Renderer


@dataclass
class Latex(_Renderer):
    """The renderer for a LaTeX table."""

    _table: _Rows
    label: str | None = None
    caption: str | None = None

    def lines(self) -> list[str]:
        """Return the string for each line of this table."""
        num_cols = len(self._table.rows[0].fields) if self._table.rows else 0
        if num_cols == 0:
            return []

        merge_spans = _calculate_merge_spans(self._table)

        lines = [
            "\\begin{table}[h]",
            "    \\centering",
        ]
        if self.label:
            lines.append(f"    \\label{{{self.label}}}")
        if self.caption:
            lines.append(f"    \\caption{{{self.caption}}}")

        lines.append(
            f"    \\begin{{tabularx}}{{\\textwidth}}{{{_construct_column_definitions(self._table)}}}"
        )

        for r, row in enumerate(self._table.rows):
            lines.append(_stringify_latex_row(r, row, merge_spans, num_cols))

        lines.append("        \\hline")
        lines.append("    \\end{tabularx}")
        lines.append("\\end{table}")

        return lines


def _calculate_merge_spans(table: _Rows) -> dict[tuple[int, int], int]:
    """Calculate vertical merge spans for multirow."""
    spans: dict[tuple[int, int], int] = {}
    if not table.rows:
        return spans

    num_cols = len(table.rows[0].fields)
    for c in range(num_cols):
        span = 1
        for r in range(len(table.rows) - 1, -1, -1):
            if r > 0:
                current = table.rows[r].fields[c]
                previous = table.rows[r - 1].fields[c]
                if (
                    current.format.merge_same
                    and previous.format.merge_same
                    and current.value == previous.value
                ):
                    span += 1
                    spans[(r, c)] = 0
                    continue
            spans[(r, c)] = span
            span = 1
    return spans


def _construct_column_definitions(table: _Rows) -> str:
    column_widths = [
        len(max(column.fields, key=lambda f: len(f.value)).value) for column in table.transpose
    ]
    widest_column_index = column_widths.index(max(column_widths))

    column_definitions = "|"
    for i in range(len(column_widths)):
        if i == widest_column_index:
            column_definitions += "X|"
        else:
            column_definitions += "l|"

    return column_definitions


def _stringify_latex_row(
    r: int, row: _Fields, merge_spans: dict[tuple[int, int], int], num_cols: int
) -> str:
    row_str = " & ".join(
        _format_field(field, merge_spans[(r, c)]) for c, field in enumerate(row.fields)
    )

    prefix = _construct_hline_or_clines(r, num_cols, merge_spans)
    if row_str.startswith(" & "):
        return f"        {prefix}{row_str} \\\\"
    return f"        {prefix} {row_str} \\\\"


def _format_field(field: _Field, span: int) -> str:
    if span == 0:
        return ""

    val = field.value
    if field.format.bold:
        val = f"\\textbf{{{val}}}"

    if field.format.align == "right":
        val = f"\\multicolumn{{1}}{{r}}{{{val}}}"
    elif field.format.align == "center":
        val = f"\\multicolumn{{1}}{{c}}{{{val}}}"

    if span > 1:
        val = f"\\multirow{{{span}}}{{*}}{{{val}}}"

    return val


def _construct_hline_or_clines(
    r: int, num_cols: int, merge_spans: dict[tuple[int, int], int]
) -> str:
    if all(merge_spans[(r, c)] != 0 for c in range(num_cols)):
        return "\\hline"

    clines: list[str] = []
    start: int | None = None
    for c in range(num_cols):
        if merge_spans[(r, c)] != 0:
            if start is None:
                start = c + 1
        elif start is not None:
            clines.append(f"\\cline{{{start}-{c}}}")
            start = None

    if start is not None:
        clines.append(f"\\cline{{{start}-{num_cols}}}")

    return " ".join(clines)
