from tablix import Table


def test_simple():
    markdown = Table.from_list([["col1", "col2"], ["value1", "val2"]]).to_markdown()

    assert markdown.lines() == [
        "| col1   | col2 |",
        "| ------ | ---- |",
        "| value1 | val2 |",
    ]
