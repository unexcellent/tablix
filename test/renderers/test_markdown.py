from tablix import Table, Format


def test_simple():
    rendered_table = Table.from_list(
        [["col1", "col2"], ["value1", "val2"], ["value3", "val4"]]
    ).to_markdown()

    assert rendered_table.lines() == [
        "| col1   | col2 |",
        "| :----- | :--- |",
        "| value1 | val2 |",
        "| value3 | val4 |",
    ]


def test_bold():
    rendered_table = Table.from_list(
        [["col1", "col2"], [("value1", Format(bold=True)), "val2"], ["value3", "val4"]]
    ).to_markdown()

    assert rendered_table.lines() == [
        "| col1       | col2 |",
        "| :--------- | :--- |",
        "| **value1** | val2 |",
        "| value3     | val4 |",
    ]


def test_align_left():
    rendered_table = Table.from_list(
        [["col1", "col2"], [("value1", Format(align="left")), "val2"], ["very_long_value", "val4"]]
    ).to_markdown()

    assert rendered_table.lines() == [
        "| col1            | col2 |",
        "| :-------------- | :--- |",
        "| value1          | val2 |",
        "| very_long_value | val4 |",
    ]


def test_align_left_when_not_all_fields_in_table_are_aligned_differently():
    rendered_table = Table.from_list(
        [
            [("col1", Format(align="center")), "col2"],
            [("value1", Format(align="right")), "val2"],
            [("very_long_value", Format(align="left")), "val4"],
        ]
    ).to_markdown()

    assert rendered_table.lines() == [
        "|      col1       | col2 |",
        "| :-------------- | :--- |",
        "|          value1 | val2 |",
        "| very_long_value | val4 |",
    ]


def test_align_entire_column_right():
    rendered_table = Table.from_list(
        [
            [("col1", Format(align="right")), "col2"],
            [("value1", Format(align="right")), "val2"],
            [("very_long_value", Format(align="right")), "val4"],
        ]
    ).to_markdown()

    assert rendered_table.lines() == [
        "|            col1 | col2 |",
        "| --------------: | :--- |",
        "|          value1 | val2 |",
        "| very_long_value | val4 |",
    ]


def test_align_entire_column_center():
    rendered_table = Table.from_list(
        [
            [("col1", Format(align="center")), "col2"],
            [("value1", Format(align="center")), "val2"],
            [("very_long_value", Format(align="center")), "val4"],
        ]
    ).to_markdown()

    assert rendered_table.lines() == [
        "|      col1       | col2 |",
        "| :-------------: | :--- |",
        "|     value1      | val2 |",
        "| very_long_value | val4 |",
    ]


def test_merge_two_fields():
    rendered_table = Table.from_list(
        [
            ["col1", "col2"],
            [("value1", Format(merge_same=True)), "val2"],
            [("value1", Format(merge_same=True)), "val4"],
            ["value5", "val6"],
        ]
    ).to_markdown()

    assert rendered_table.lines() == [
        "| col1   | col2 |",
        "| :----- | :--- |",
        "| value1 | val2 |",
        "|        | val4 |",
        "| value5 | val6 |",
    ]


def test_merge_three_fields():
    rendered_table = Table.from_list(
        [
            ["col1", "col2"],
            [("value1", Format(merge_same=True)), "val2"],
            [("value1", Format(merge_same=True)), "val4"],
            [("value1", Format(merge_same=True)), "val6"],
        ]
    ).to_markdown()

    assert rendered_table.lines() == [
        "| col1   | col2 |",
        "| :----- | :--- |",
        "| value1 | val2 |",
        "|        | val4 |",
        "|        | val6 |",
    ]
