import re
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import validate_hld

TEMPLATE_TEXT = validate_hld.TEMPLATE.read_text(encoding="utf-8")
DIAGRAM = "```mermaid\nflowchart LR\n  A --> B\n```\n"
SECURITY_TEXT = "CIS Controls v8.1 Implementation Group 3, CIS Benchmark for Kubernetes v1.10 Level 2.\n\n"
LINKS ="".join(f"- [Source {i}](https://example.org/{i}) accessed 2026-09-16\n" for i in range(5))

def valid_hld():
    text = re.sub(r"\{\{.*?\}\}", "Content.", TEMPLATE_TEXT, flags=re.DOTALL)
    text = text.replace("## 6. Solution Overview\n", "## 6. Solution Overview\n\n" + DIAGRAM + DIAGRAM)
    text = text.replace("## 10. Security Architecture\n", "## 10. Security Architecture\n\n" + SECURITY_TEXT)
    return text.replace("## 21. References\n", "## 21. References\n\n" + LINKS)

class ValidateHldTest(unittest.TestCase):
    def test_valid_document_passes(self):
        self.assertEqual(validate_hld.validate(valid_hld(), TEMPLATE_TEXT), [])

    def test_unfilled_template_fails(self):
        issues = validate_hld.validate(TEMPLATE_TEXT, TEMPLATE_TEXT)
        self.assertTrue(any("placeholder" in issue for issue in issues))
        self.assertTrue(any("Mermaid" in issue for issue in issues))
        self.assertTrue(any("References" in issue for issue in issues))

    def test_missing_section(self):
        text = valid_hld().replace("## 20. Glossary", "## 20. Terms")
        self.assertIn("missing section: Glossary", validate_hld.validate(text, TEMPLATE_TEXT))

    def test_section_out_of_order(self):
        text = valid_hld()
        glossary = "## 20. Glossary\n\nContent.\n\n"
        text = text.replace(glossary, "").replace("## 2. Executive Summary", glossary + "## 2. Executive Summary")
        self.assertTrue(any("out of order" in issue for issue in validate_hld.validate(text, TEMPLATE_TEXT)))

    def test_empty_section(self):
        text = valid_hld().replace("## 20. Glossary\n\nContent.", "## 20. Glossary\n")
        self.assertTrue(any("empty section: Glossary" in issue for issue in validate_hld.validate(text, TEMPLATE_TEXT)))

    def test_missing_itil_practice(self):
        text = valid_hld().replace("| Problem management |", "| Something else |")
        issues = validate_hld.validate(text, TEMPLATE_TEXT)
        self.assertIn("ITIL table missing practice: Problem management", issues)

    def test_missing_security_function(self):
        text = valid_hld().replace("| Detect |", "| Watch |")
        issues = validate_hld.validate(text, TEMPLATE_TEXT)
        self.assertIn("security control mapping missing function: Detect", issues)

    def test_missing_cis_implementation_group(self):
        text = valid_hld().replace("Implementation Group 3", "IG3")
        issues = validate_hld.validate(text, TEMPLATE_TEXT)
        self.assertIn("Security Architecture does not mention: Implementation Group", issues)

    def test_heading_inside_code_block_is_ignored(self):
        text = valid_hld().replace(DIAGRAM, "```mermaid\n## 99. Not A Section\n```\n", 1)
        self.assertEqual(validate_hld.validate(text, TEMPLATE_TEXT), [])

class CommandLineTest(unittest.TestCase):
    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / "validate_hld.py"), *args], capture_output=True, text=True)

    def test_usage_error(self):
        self.assertEqual(self.run_script().returncode, 2)

    def test_missing_file(self):
        self.assertEqual(self.run_script("does-not-exist.md").returncode, 2)

    def test_findings_exit_code(self):
        result = self.run_script(str(validate_hld.TEMPLATE))
        self.assertEqual(result.returncode, 1)
        self.assertIn("placeholder", result.stdout)

if __name__ == '__main__':
    unittest.main()
