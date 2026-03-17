from __future__ import annotations

from dataclasses import dataclass

from tablix._core import _Field, _Fields, _Rows
from tablix.format import Format
from tablix.renderers.latex import Latex
from tablix.renderers.markdown import Markdown
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
        """Construct a Table from a list.

        Args:
            content: Matrix of values in this table. The first index represents the rows and the
                second index the columns. The first row is always the header row. Field values can
                either be a value directly of a tuple of a value and a `tablix.Format`.
            column_formats: Specify formatting for entire columns. Dict keys are the column indices
                (0 is the leftmost column) and values are the `tablix.Format` to be applied.
            row_formats: Specify formatting for entire rows. Dict keys are the row indices
                (0 is the header column) and values are the `tablix.Format` to be applied.

        Returns:
            The constructed table.

        Examples:
            This constructor is probably the most straight forward way of constructing a Table.
            ```python
            from tablix import Table

            table = Table.from_list(
                [
                    ["Item", "Price"],
                    ["Beer", 1.14],
                    ["Pretzels", 10.89],
                ]
            )
            print(table)
            ```
            ```bash
            ╭──────────┬───────╮
            │ Item     │ Price │
            ┝━━━━━━━━━━┿━━━━━━━┥
            │ Beer     │ 1.14  │
            ├──────────┼───────┤
            │ Pretzels │ 10.89 │
            ╰──────────┴───────╯
            ```

            You can specify formatting per field
            ```python
            from tablix import Table, Format

            table = Table.from_list(
                [
                    ["Item", "Price"],
                    [("Beer", Format(align="right")), 1.14],
                    ["Pretzels", 10.89],
                ]
            )
            print(table)
            ```
            ```bash
            ╭──────────┬───────╮
            │ Item     │ Price │
            ┝━━━━━━━━━━┿━━━━━━━┥
            │     Beer │ 1.14  │
            ├──────────┼───────┤
            │ Pretzels │ 10.89 │
            ╰──────────┴───────╯
            ```

            per row
            ```python
            from tablix import Table, Format

            table = Table.from_list(
                [
                    ["Item", "Price"],
                    ["Beer", 1.14],
                    ["Pretzels", 10.89],
                ],
                row_formats={0: Format(align="right")},
            )
            print(table)
            ```
            ```bash
            ╭──────────┬───────╮
            │ Item     │ Price │
            ┝━━━━━━━━━━┿━━━━━━━┥
            │     Beer │  1.14 │
            ├──────────┼───────┤
            │ Pretzels │ 10.89 │
            ╰──────────┴───────╯
            ```

            or per column.
            ```python
            from tablix import Table, Format

            table = Table.from_list(
                [
                    ["Item", "Price"],
                    ["Beer", 1.14],
                    ["Pretzels", 10.89],
                ],
                column_formats={0: Format(align="right")},
            )
            print(table)
            ```
            ```bash
            ╭──────────┬───────╮
            │     Item │ Price │
            ┝━━━━━━━━━━┿━━━━━━━┥
            │     Beer │ 1.14  │
            ├──────────┼───────┤
            │ Pretzels │ 10.89 │
            ╰──────────┴───────╯
            ```

        """
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

    def to_latex(self, label: str | None = None, caption: str | None = None) -> Latex:
        """Convert this table to LaTeX format."""
        return Latex(self._rows, label, caption)

    def to_markdown(self) -> Markdown:
        """Convert this table to Markdown format."""
        return Markdown(self._rows)

    def __str__(self) -> str:
        return self.to_terminal().__str__()
