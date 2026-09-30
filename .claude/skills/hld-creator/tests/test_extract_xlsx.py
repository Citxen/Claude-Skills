import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import extract_xlsx

WORKBOOK = """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="Discovery register" sheetId="1" r:id="rId1"/><sheet name="Dashboard" sheetId="2" r:id="rId2"/></sheets>
</workbook>"""

RELS = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Target="worksheets/sheet2.xml"/>
</Relationships>"""

SHARED = """<?xml version="1.0" encoding="UTF-8"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<si><t>ID</t></si><si><t>Question</t></si><si><t>A01</t></si><si><t>Which cloud | environment?</t></si>
</sst>"""

# Row 2 skips column B to prove gaps are preserved; the inline string exercises the other text path
SHEET1 = """<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>
<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1" t="s"><v>1</v></c></row>
<row r="2"><c r="A2" t="s"><v>2</v></c><c r="C2" t="s"><v>3</v></c></row>
<row r="3"></row>
<row r="4"><c r="A4" t="inlineStr"><is><t>Inline value</t></is></c></row>
</sheetData></worksheet>"""

# Formulas with no cached value: bare, and with the empty <v/> that openpyxl writes
SHEET2 = """<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>
<row r="1"><c r="A1"><f>COUNTIF(B:B,"Open")</f></c><c r="B1"><v>42</v></c></row>
<row r="2"><c r="A2"><f>SUM(B1:B1)</f><v /></c></row>
</sheetData></worksheet>"""

class ExtractXlsxTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name) / "example.xlsx"
        with zipfile.ZipFile(self.path, "w") as archive:
            archive.writestr("xl/workbook.xml", WORKBOOK)
            archive.writestr("xl/_rels/workbook.xml.rels", RELS)
            archive.writestr("xl/sharedStrings.xml", SHARED)
            archive.writestr("xl/worksheets/sheet1.xml", SHEET1)
            archive.writestr("xl/worksheets/sheet2.xml", SHEET2)

    def tearDown(self):
        self.directory.cleanup()

    def test_sheets_in_workbook_order(self):
        text = extract_xlsx.extract(self.path)
        self.assertLess(text.index("## Discovery register"), text.index("## Dashboard"))

    def test_shared_strings_and_header_separator(self):
        text = extract_xlsx.extract(self.path)
        self.assertIn("| ID | Question |", text)
        self.assertIn("|---|---|---|", text)

    def test_pipe_is_escaped(self):
        self.assertIn("Which cloud \\| environment?", extract_xlsx.extract(self.path))

    def test_missing_cell_keeps_its_column(self):
        # A2 is populated, B2 is absent, C2 is populated
        self.assertIn("| A01 |  | Which cloud", extract_xlsx.extract(self.path))

    def test_empty_row_is_dropped(self):
        self.assertNotIn("|  |  |  |", extract_xlsx.extract(self.path))

    def test_inline_string(self):
        self.assertIn("Inline value", extract_xlsx.extract(self.path))

    def test_formula_without_cached_value_shows_the_formula(self):
        self.assertIn('=COUNTIF(B:B,"Open")', extract_xlsx.extract(self.path))

    def test_formula_with_an_empty_cached_value_shows_the_formula(self):
        # openpyxl writes <f>...</f><v/>, which must not read as a blank cell
        self.assertIn("=SUM(B1:B1)", extract_xlsx.extract(self.path))

    def test_single_sheet_filter(self):
        text = extract_xlsx.extract(self.path, "dashboard")
        self.assertIn("## Dashboard", text)
        self.assertNotIn("## Discovery register", text)

    def test_column_index(self):
        self.assertEqual(extract_xlsx.column_index("A1"), 0)
        self.assertEqual(extract_xlsx.column_index("Z9"), 25)
        self.assertEqual(extract_xlsx.column_index("AB12"), 27)

class CommandLineTest(unittest.TestCase):
    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / "extract_xlsx.py"), *args],
                              capture_output=True, text=True)

    def test_usage_error(self):
        self.assertEqual(self.run_script().returncode, 2)

    def test_not_an_xlsx(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "not.xlsx"
            path.write_text("plain text", encoding="utf-8")
            self.assertEqual(self.run_script(str(path)).returncode, 1)

if __name__ == '__main__':
    unittest.main()
