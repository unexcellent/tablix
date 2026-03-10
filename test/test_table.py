from tablix import Table, Field, Format


def test_from_list_simple_with_headers():
    table = Table.from_list(headers=["col1", "col2"], content=[["f11", "f12"], ["f21", "f22"]])

    assert table.headers == [Field("col1", Format()), Field("col2", Format())]
    assert table.content == [
        [Field("f11", Format()), Field("f12", Format())],
        [Field("f21", Format()), Field("f22", Format())],
    ]


def test_from_list_simple_without_headers():
    table = Table.from_list([["col1", "col2"], ["f11", "f12"], ["f21", "f22"]])

    assert table.headers == [Field("col1", Format()), Field("col2", Format())]
    assert table.content == [
        [Field("f11", Format()), Field("f12", Format())],
        [Field("f21", Format()), Field("f22", Format())],
    ]
