from tablix import Table, Field, Format


def test_from_list_simple_with_headers():
    default = Format.default()
    table = Table.from_list(headers=["col1", "col2"], content=[["f11", "f12"], ["f21", "f22"]])

    assert table.headers == [Field("col1", default), Field("col2", default)]
    assert table.content == [
        [Field("f11", default), Field("f12", default)],
        [Field("f21", default), Field("f22", default)],
    ]


def test_from_list_simple_without_headers():
    default = Format.default()
    table = Table.from_list([["col1", "col2"], ["f11", "f12"], ["f21", "f22"]])

    assert table.headers == [Field("col1", default), Field("col2", default)]
    assert table.content == [
        [Field("f11", default), Field("f12", default)],
        [Field("f21", default), Field("f22", default)],
    ]


def test_from_list_with_field_specific_formatting():
    default = Format.default()
    bold = Format(bold=True)
    table = Table.from_list([[("col1", bold), "col2"], [("f1", bold), "f2"]])

    assert table.headers == [Field("col1", bold), Field("col2", default)]
    assert table.content == [[Field("f1", bold), Field("f2", default)]]


def test_from_list_with_column_specific_formatting():
    default = Format.default()
    bold = Format(bold=True)
    table = Table.from_list(
        [["col1", "col2"], ["f11", "f12"], ["f21", "f22"]], column_formats={0: bold}
    )

    assert table.headers == [Field("col1", bold), Field("col2", default)]
    assert table.content == [
        [Field("f11", bold), Field("f12", default)],
        [Field("f21", bold), Field("f22", default)],
    ]


def test_field_formatting_beats_column_formatting():
    default = Format.default()
    bold = Format(bold=True)
    table = Table.from_list(
        [["col1", "col2"], [("f11", default), "f12"], ["f21", "f22"]], column_formats={0: bold}
    )

    assert table.headers == [Field("col1", bold), Field("col2", default)]
    assert table.content == [
        [Field("f11", default), Field("f12", default)],
        [Field("f21", bold), Field("f22", default)],
    ]


def test_from_list_with_row_specific_formatting():
    default = Format.default()
    bold = Format(bold=True)
    table = Table.from_list(
        [["col1", "col2"], ["f11", "f12"], ["f21", "f22"]], row_formats={1: bold}
    )

    assert table.headers == [Field("col1", default), Field("col2", default)]
    assert table.content == [
        [Field("f11", bold), Field("f12", bold)],
        [Field("f21", default), Field("f22", default)],
    ]


def test_field_formatting_beats_row_formatting():
    default = Format.default()
    bold = Format(bold=True)
    table = Table.from_list(
        [["col1", "col2"], [("f11", default), "f12"], ["f21", "f22"]], row_formats={1: bold}
    )

    assert table.headers == [Field("col1", default), Field("col2", default)]
    assert table.content == [
        [Field("f11", default), Field("f12", bold)],
        [Field("f21", default), Field("f22", default)],
    ]


def test_row_formatting_beats_column_formatting():
    default = Format.default()
    bold = Format(bold=True)
    italic = Format(italic=True)
    table = Table.from_list(
        [["col1", "col2"], ["f11", "f12"], ["f21", "f22"]],
        column_formats={0: bold},
        row_formats={1: italic},
    )

    assert table.headers == [Field("col1", bold), Field("col2", default)]
    assert table.content == [
        [Field("f11", italic), Field("f12", italic)],
        [Field("f21", bold), Field("f22", default)],
    ]
