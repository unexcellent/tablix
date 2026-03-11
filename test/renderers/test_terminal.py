from tablix import Table, Format


def test_simple_no_bold_headers():
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
