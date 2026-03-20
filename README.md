A python package for complex tables with fine-grained formatting.

# Installation

# Standout Features

Yes, this is yet another table renderer in python just like [`tabulate`](https://github.com/astanin/python-tabulate), [`prettytable`](https://github.com/prettytable/prettytable) and many others. However, this one has some unique features that the others lack.

- **Fine-Grained Formatting**: You can apply formatting to entire rows, columns or on a per field basis. Want to highlight a specific field by making it bold? No problem. Boss wants the header row extra special? Let him have it.
- **Field Merging**: With tablix you can you can merge multiple consecutive fields in the same column. This is especially usefull to signify multiple rows belong to the same category.

In short

| **Feature**                  | **Tablix**    | **Others** |
| :--------------------------- | :------------ | :--------- |
| Rendering in Dozens of Forms | **No**        | Yes        |
| Years of Bugfixing           | **No**        | Yes        |
| Robust Community Support     | **No**        | Yes        |
| Fine-Grained Formatting      | **Hell Yeah** | No         |

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

