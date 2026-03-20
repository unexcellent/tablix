from __future__ import annotations

from dataclasses import dataclass

from tablix._core import _Field, _Fields, _Rows
from tablix.format import Format
from tablix.renderers.latex import Latex
from tablix.renderers.markdown import Markdown
from tablix.renderers.terminal import Terminal


@dataclass
class Table:
    r"""The class representation of a table.

    Construct a `Table` using `Table.from_list()` and then convert it into a rendered format using
    `Table.to_[rendered_format]().lines()`.


    # Examples

    ## Basic Formatting

    By default, a table can be constructed with just items. In this case basic formatting is applied.
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

    Formatting can either be applied per field, per row and/or per column. If those formats overlap,
    field formatting is applied over row formatting which is applied over column formatting.
    ```python
    from tablix import Table, Format

    print(Table.from_list(
        [
            ["Item", "Price"],
            [("Beer", Format(align="right")), 1.14],
            ["Pretzels", 10.89],
        ]
    ))
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
    ```python
    print(Table.from_list(
        [
            ["Item", "Price"],
            ["Beer", 1.14],
            ["Pretzels", 10.89],
        ],
        row_formats={1: Format(align="right")},
    ))
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
    ```python
    print(Table.from_list(
        [
            ["Item", "Price"],
            ["Beer", 1.14],
            ["Pretzels", 10.89],
        ],
        column_formats={0: Format(align="right")},
    ))
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

    ## Combining Fields

    The standout feature from `tablix` is the possibility to combine multiple fields of a single
    column. This is also handled by the formatting system. All adjacent fields in a single column
    which have the same value and a `Format` with `merge_same=True` are merged into a single cell
    spanning multiple rows.
    ```python
    from tablix import Table, Format

    print(Table.from_list(
        [
            ["Category", "Item", "Price"],
            ["Food", "Brathendl", 10.89],
            ["Food", "Pretzels", 0.55],
            ["Drinks", "Beer", 1.14],
            ["Drinks", "Spezi", 0.89],
        ],
        column_formats={0: Format(merge_same=True)},
    ))
    ```
    ```bash
    ╭──────────┬───────────┬───────╮
    │ Category │ Item      │ Price │
    ┝━━━━━━━━━━┿━━━━━━━━━━━┿━━━━━━━┥
    │ Food     │ Brathendl │ 10.89 │
    │          ├───────────┼───────┤
    │          │ Pretzels  │ 0.55  │
    ├──────────┼───────────┼───────┤
    │ Drinks   │ Beer      │ 1.14  │
    │          ├───────────┼───────┤
    │          │ Spezi     │ 0.89  │
    ╰──────────┴───────────┴───────╯
    ```

    ## Output Formats

    A `Table` can be converted to a rendered format using `Table.to_[rendered format]()`. This
    returns an object with the type of the renderer. To get the individual rendered lines call
    `Table.to_[rendered format]().lines()`. To write the lines directly into a file call
    `Table.to_[rendered format]().write_to(path)`.
    ```python
    from tablix import Table

    table = Table.from_list(
        [
            ["Item", "Price"],
            ["Beer", 1.14],
            ["Pretzels", 10.89],
        ]
    )
    rendered_table = table.to_[rendered_format]()
    lines: list[str] = rendered_table.lines()
    string: str = str(rendered_table)
    rendered_table.write_to(path)  # write directly to a file
    ```

    ### Terminal

    ```python
    from tablix import Table

    table = Table.from_list(
        [
            ["Item", "Price"],
            ["Beer", 1.14],
            ["Pretzels", 10.89],
        ]
    )
    rendered_table = table.to_terminal()
    print(rendered_table)
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

    ### Markdown

    ```python
    from tablix import Table

    table = Table.from_list(
        [
            ["Item", "Price"],
            ["Beer", 1.14],
            ["Pretzels", 10.89],
        ]
    )
    rendered_table = table.to_markdown()
    print(rendered_table)
    ```
    ```bash
    | Item     | Price |
    | :------- | :---- |
    | Beer     | 1.14  |
    | Pretzels | 10.89 |
    ```

    ### Latex

    ```python
    from tablix import Table

    table = Table.from_list(
        [
            ["Item", "Price"],
            ["Beer", 1.14],
            ["Pretzels", 10.89],
        ]
    )
    rendered_table = table.to_latex()
    print(rendered_table)
    ```
    ```bash
    \begin{table}[h]
        \centering
        \begin{tabularx}{\textwidth}{|X|l|}
            \hline Item & Price \\
            \hline Beer & 1.14 \\
            \hline Pretzels & 10.89 \\
            \hline
        \end{tabularx}
    \end{table}
    ```
    """

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
