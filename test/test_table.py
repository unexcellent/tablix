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
    table = Table.from_list([[("col1", bold), "col2"], [("f1", bold), "f1"]])

    assert table.headers == [Field("col1", bold), Field("col2", default)]
    assert table.content == [[Field("f1", bold), Field("f1", default)]]
