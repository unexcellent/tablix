from tablix import Table, Format
from tablix._core import _Rows, _Fields, _Field


def test_from_list_simple():
    default = Format.default()
    table = Table.from_list([["col1", "col2"], ["f11", "f12"], ["f21", "f22"]])

    assert table._rows == _Rows(
        [
            _Fields([_Field("col1", default), _Field("col2", default)]),
            _Fields([_Field("f11", default), _Field("f12", default)]),
            _Fields([_Field("f21", default), _Field("f22", default)]),
        ]
    )


def test_from_list_with_field_specific_formatting():
    default = Format.default()
    bold = Format(bold=True)
    table = Table.from_list([[("col1", bold), "col2"], [("f11", default), "f12"], ["f21", "f22"]])

    assert table._rows == _Rows(
        [
            _Fields([_Field("col1", bold), _Field("col2", default)]),
            _Fields([_Field("f11", default), _Field("f12", default)]),
            _Fields([_Field("f21", default), _Field("f22", default)]),
        ]
    )


def test_from_list_with_column_specific_formatting():
    default = Format.default()
    bold = Format(bold=True)
    table = Table.from_list(
        [[("col1", bold), "col2"], ["f11", "f12"], ["f21", "f22"]],
        column_formats={0: bold},
    )

    assert table._rows == _Rows(
        [
            _Fields([_Field("col1", bold), _Field("col2", default)]),
            _Fields([_Field("f11", bold), _Field("f12", default)]),
            _Fields([_Field("f21", bold), _Field("f22", default)]),
        ]
    )


def test_field_formatting_beats_column_formatting():
    default = Format.default()
    bold = Format(bold=True)
    table = Table.from_list(
        [["col1", "col2"], [("f11", default), "f12"], ["f21", "f22"]], column_formats={0: bold}
    )

    assert table._rows == _Rows(
        [
            _Fields([_Field("col1", bold), _Field("col2", default)]),
            _Fields([_Field("f11", default), _Field("f12", default)]),
            _Fields([_Field("f21", bold), _Field("f22", default)]),
        ]
    )


def test_from_list_with_row_specific_formatting():
    default = Format.default()
    bold = Format(bold=True)
    table = Table.from_list(
        [["col1", "col2"], ["f11", "f12"], ["f21", "f22"]], row_formats={1: bold}
    )

    assert table._rows == _Rows(
        [
            _Fields([_Field("col1", default), _Field("col2", default)]),
            _Fields([_Field("f11", bold), _Field("f12", bold)]),
            _Fields([_Field("f21", default), _Field("f22", default)]),
        ]
    )


def test_field_formatting_beats_row_formatting():
    default = Format.default()
    bold = Format(bold=True)
    table = Table.from_list(
        [["col1", "col2"], [("f11", default), "f12"], ["f21", "f22"]], row_formats={1: bold}
    )

    assert table._rows == _Rows(
        [
            _Fields([_Field("col1", default), _Field("col2", default)]),
            _Fields([_Field("f11", default), _Field("f12", bold)]),
            _Fields([_Field("f21", default), _Field("f22", default)]),
        ]
    )


def test_row_formatting_beats_column_formatting():
    default = Format.default()
    bold = Format(bold=True)
    italic = Format(italic=True)
    table = Table.from_list(
        [["col1", "col2"], ["f11", "f12"], ["f21", "f22"]],
        column_formats={0: bold},
        row_formats={1: italic},
    )

    assert table._rows == _Rows(
        [
            _Fields([_Field("col1", bold), _Field("col2", default)]),
            _Fields([_Field("f11", italic), _Field("f12", italic)]),
            _Fields([_Field("f21", bold), _Field("f22", default)]),
        ]
    )


def test_auto_alignment_based_on_type():
    default = Format.default()
    left = Format(align="left")
    right = Format(align="right")
    table = Table.from_list(
        [["col1", "col2"], ["f11", 12], [True, 3.14]],
    )

    assert table._rows == _Rows(
        [
            _Fields([_Field("col1", default), _Field("col2", default)]),
            _Fields([_Field("f11", default), _Field("12", right)]),
            _Fields([_Field("True", left), _Field("3.14", left)]),
        ]
    )
