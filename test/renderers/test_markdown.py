from tablix import Table, Format


def test_simple():
    markdown = Table.from_list([["col1", "col2"], ["value1", "val2"]]).to_markdown()

    assert markdown.lines() == [
        "| col1   | col2 |",
        "| ------ | ---- |",
        "| value1 | val2 |",
    ]


def test_bold():
    markdown = Table.from_list(
        [[("col1", Format(bold=True)), "col2"], ["value1", "val2"]]
    ).to_markdown()

    assert markdown.lines() == [
        "| **col1** | col2 |",
        "| -------- | ---- |",
        "| value1   | val2 |",
    ]


def test_italic():
    markdown = Table.from_list(
        [[("col1", Format(italic=True)), "col2"], ["value1", "val2"]]
    ).to_markdown()

    assert markdown.lines() == [
        "| __col1__ | col2 |",
        "| -------- | ---- |",
        "| value1   | val2 |",
    ]
