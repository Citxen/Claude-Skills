import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import extract_docx

DOCUMENT = """<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>
<w:p><w:pPr><w:pStyle w:val="Title"/></w:pPr><w:r><w:t>Payments HLD</w:t></w:r></w:p>
<w:p><w:pPr><w:pStyle w:val="Heading2"/></w:pPr><w:r><w:t>Scope</w:t></w:r></w:p>
<w:p><w:r><w:t xml:space="preserve">Covers card </w:t></w:r><w:r><w:t>payments.</w:t></w:r></w:p>
<w:p></w:p>
<w:tbl>
<w:tr><w:tc><w:p><w:r><w:t>ID</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Requirement</w:t></w:r></w:p></w:tc></w:tr>
<w:tr><w:tc><w:p><w:r><w:t>NFR-01</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>99.99% | monthly</w:t></w:r></w:p></w:tc></w:tr>
</w:tbl>
<w:sdt><w:sdtContent><w:p><w:r><w:t>Inside a content control</w:t></w:r></w:p></w:sdtContent></w:sdt>
</w:body></w:document>"""

EXPECTED = """# Payments HLD

## Scope

Covers card payments.

| ID | Requirement |
|---|---|
| NFR-01 | 99.99% \\| monthly |

Inside a content control"""

class ExtractDocxTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name) / "example.docx"
        with zipfile.ZipFile(self.path, "w") as archive:
            archive.writestr("word/document.xml", DOCUMENT)

    def tearDown(self):
        self.directory.cleanup()

    def test_extracts_headings_paragraphs_tables_and_content_controls(self):
        self.assertEqual(extract_docx.extract(self.path), EXPECTED)

    def test_command_line_prints_markdown(self):
        result = subprocess.run([sys.executable, str(SCRIPTS / "extract_docx.py"), str(self.path)],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), EXPECTED)

    def test_not_a_docx(self):
        not_docx = Path(self.directory.name) / "notes.docx"
        not_docx.write_text("plain text", encoding="utf-8")
        result = subprocess.run([sys.executable, str(SCRIPTS / "extract_docx.py"), str(not_docx)], capture_output=True)
        self.assertEqual(result.returncode, 1)

    def test_usage_error(self):
        result = subprocess.run([sys.executable, str(SCRIPTS / "extract_docx.py")], capture_output=True)
        self.assertEqual(result.returncode, 2)

if __name__ == '__main__':
    unittest.main()
