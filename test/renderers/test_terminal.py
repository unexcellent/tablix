from tablix import Table, Format


def test_simple():
    rendered_table = Table.from_list(
        [["col1", "col2"], ["value1", "val2"], ["value3", "val4"]]
    ).to_terminal()

    assert rendered_table.lines() == [
        "│ col1   │ col2 │",
        "┝━━━━━━━━┿━━━━━━┥",
        "│ value1 │ val2 │",
        "├────────┼──────┤",
        "│ value3 │ val4 │",
    ]


def test_bold():
    rendered_table = Table.from_list(
        [["col1", "col2"], [("value1", Format(bold=True)), "val2"], ["value3", "val4"]]
    ).to_terminal()

    assert rendered_table.lines() == [
        "│ col1   │ col2 │",
        "┝━━━━━━━━┿━━━━━━┥",
        "│ \033[1mvalue1\033[0m │ val2 │",  # column width looks weird here but is fine when printing
        "├────────┼──────┤",
        "│ value3 │ val4 │",
    ]
