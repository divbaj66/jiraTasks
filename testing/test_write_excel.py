# ...existing code...
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import openpyxl
from openpyxl import Workbook
import tempfile
from write_excel import write_to_excel
import pytest
from io import StringIO
import builtins

def test_write_to_excel_overwrites_rows_and_appends(tmp_path, capsys):
    # Create a workbook with header and one data row
    fp = tmp_path / "test.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "DOD Staging"
    ws.append(["ID", "Title"])         # header
    ws.append(["OLD-1", "Old Title"])  # old row to be removed
    wb.save(fp)

    # New data rows (each row should be an iterable)
    new_rows = [
        ["JA-1", "New title 1"],
        ["JA-2", "New title 2"]
    ]

    write_to_excel(str(fp), new_rows)

    # Reload workbook and assert rows
    wb2 = openpyxl.load_workbook(str(fp))
    ws2 = wb2["DOD Staging"]
    rows = list(ws2.values)
    # header + 2 new rows == 3 rows total
    assert rows[0] == ("ID", "Title")
    assert rows[1] == tuple(new_rows[0])
    assert rows[2] == tuple(new_rows[1])

    captured = capsys.readouterr()
    assert "✅ Data written to" in captured.out