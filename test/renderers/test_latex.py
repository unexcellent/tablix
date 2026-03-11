from tablix import Table, Format


def test_simple():
    rendered_table = Table.from_list(
        [["col1", "column2"], ["value1", "val2"], ["value3", "val4"]]
    ).to_latex()

    assert rendered_table.lines() == [
        "\\begin{table}[h]",
        "    \\centering",
        "    \\begin{tabularx}{\\textwidth}{|l|X|}",
        "        \\hline col1 & column2 \\\\",
        "        \\hline value1 & val2 \\\\",
        "        \\hline value3 & val4 \\\\",
        "        \\hline",
        "    \\end{tabularx}",
        "\\end{table}",
    ]


def test_label():
    rendered_table = Table.from_list(
        [["col1", "col2"], ["value1", "val2"], ["value3", "val4"]]
    ).to_latex(label="tbl:my-label")

    assert rendered_table.lines() == [
        "\\begin{table}[h]",
        "    \\centering",
        "    \\label{tbl:my-label}",
        "    \\begin{tabularx}{\\textwidth}{|X|l|}",
        "        \\hline col1 & col2 \\\\",
        "        \\hline value1 & val2 \\\\",
        "        \\hline value3 & val4 \\\\",
        "        \\hline",
        "    \\end{tabularx}",
        "\\end{table}",
    ]


def test_caption():
    rendered_table = Table.from_list(
        [["col1", "col2"], ["value1", "val2"], ["value3", "val4"]]
    ).to_latex(caption="My Nice Table")

    assert rendered_table.lines() == [
        "\\begin{table}[h]",
        "    \\centering",
        "    \\caption{My Nice Table}",
        "    \\begin{tabularx}{\\textwidth}{|X|l|}",
        "        \\hline col1 & col2 \\\\",
        "        \\hline value1 & val2 \\\\",
        "        \\hline value3 & val4 \\\\",
        "        \\hline",
        "    \\end{tabularx}",
        "\\end{table}",
    ]


def test_bold():
    rendered_table = Table.from_list(
        [["col1", "col2"], [("value1", Format(bold=True)), "val2"], ["value3", "val4"]]
    ).to_latex()

    assert rendered_table.lines() == [
        "\\begin{table}[h]",
        "    \\centering",
        "    \\begin{tabularx}{\\textwidth}{|X|l|}",
        "        \\hline col1 & col2 \\\\",
        "        \\hline \\textbf{value1} & val2 \\\\",
        "        \\hline value3 & val4 \\\\",
        "        \\hline",
        "    \\end{tabularx}",
        "\\end{table}",
    ]


def test_align_right():
    rendered_table = Table.from_list(
        [["col1", "col2"], [("value1", Format(align="right")), "val2"], ["very_long_value", "val4"]]
    ).to_latex()

    assert rendered_table.lines() == [
        "\\begin{table}[h]",
        "    \\centering",
        "    \\begin{tabularx}{\\textwidth}{|X|l|}",
        "        \\hline col1 & col2 \\\\",
        "        \\hline \\multicolumn{1}{r}{value1} & val2 \\\\",
        "        \\hline very_long_value & val4 \\\\",
        "        \\hline",
        "    \\end{tabularx}",
        "\\end{table}",
    ]


def test_align_center():
    rendered_table = Table.from_list(
        [
            ["col1", "col2"],
            [("value1", Format(align="center")), "val2"],
            ["very_long_value", "val4"],
        ]
    ).to_latex()

    assert rendered_table.lines() == [
        "\\begin{table}[h]",
        "    \\centering",
        "    \\begin{tabularx}{\\textwidth}{|X|l|}",
        "        \\hline col1 & col2 \\\\",
        "        \\hline \\multicolumn{1}{c}{value1} & val2 \\\\",
        "        \\hline very_long_value & val4 \\\\",
        "        \\hline",
        "    \\end{tabularx}",
        "\\end{table}",
    ]


def test_merge_two_fields():
    rendered_table = Table.from_list(
        [
            ["col1", "col2", "col3"],
            [("value1", Format(merge_same=True)), "val2", "val3"],
            [("value1", Format(merge_same=True)), "val5", "val6"],
            ["value7", "val8", "val9"],
        ]
    ).to_latex()

    assert rendered_table.lines() == [
        "\\begin{table}[h]",
        "    \\centering",
        "    \\begin{tabularx}{\\textwidth}{|X|l|l|}",
        "        \\hline col1 & col2 & col3 \\\\",
        "        \\hline \\multirow{2}{*}{value1} & val2 & val3 \\\\",
        "        \\cline{2-3} & val5 & val6 \\\\",
        "        \\hline value7 & val8 & val9 \\\\",
        "        \\hline",
        "    \\end{tabularx}",
        "\\end{table}",
    ]


def test_merge_three_fields():
    rendered_table = Table.from_list(
        [
            ["col1", "col2", "col3"],
            [("value1", Format(merge_same=True)), "val2", "val3"],
            [("value1", Format(merge_same=True)), "val5", "val6"],
            [("value1", Format(merge_same=True)), "val8", "val9"],
        ]
    ).to_latex()

    assert rendered_table.lines() == [
        "\\begin{table}[h]",
        "    \\centering",
        "    \\begin{tabularx}{\\textwidth}{|X|l|l|}",
        "        \\hline col1 & col2 & col3 \\\\",
        "        \\hline \\multirow{3}{*}{value1} & val2 & val3 \\\\",
        "        \\cline{2-3} & val5 & val6 \\\\",
        "        \\cline{2-3} & val8 & val9 \\\\",
        "        \\hline",
        "    \\end{tabularx}",
        "\\end{table}",
    ]
