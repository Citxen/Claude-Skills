import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import validate_pack

REGISTER_HEADERS = ["ID", "Domain", "Question or data point", "Why it matters (HLD section)",
                    "How to obtain", "Who owns the answer", "Priority", "Workshop",
                    "Flag to confirm", "Answer", "Evidence link", "Status", "Confidence"]

def question(number, domain, workshop="W1", priority="Must"):
    return [f"Q{number:03d}", domain, f"Question {number}?", "3 Scope", "Interview",
            "Service owner", priority, workshop, "", "", "", "Open", ""]

def valid_spec():
    domains = [f"Domain {index}" for index in range(1, 9)]
    rows = [question(number, domains[number % len(domains)]) for number in range(1, 65)]
    return {
        "output": "pack.xlsx",
        "sheets": [
            {"name": "Read me", "headers": ["Item", "Detail"], "rows": [["Purpose", "Gather inputs"]]},
            {"name": "Discovery register", "headers": REGISTER_HEADERS, "rows": rows},
            {"name": "Tooling", "headers": ["Tool", "What it gathers"], "rows": [["Reports", "Devices"]]},
            {"name": "Workshops", "headers": ["Ref", "Workshop"], "rows": [["W1", "Scope"]]},
            {"name": "Sources", "headers": ["#", "Source", "Published or updated", "Accessed"],
             "rows": [[index, f"Source {index}", "2026-01-01", "2026-09-30"] for index in range(1, 6)]},
            {"name": "Dashboard", "headers": ["Domain", "Questions"], "rows": [[name, "=1"] for name in domains]},
        ],
    }

class ValidatePackTest(unittest.TestCase):
    def test_valid_spec_passes(self):
        self.assertEqual(validate_pack.validate(valid_spec()), [])

    def test_missing_sheet(self):
        spec = valid_spec()
        spec["sheets"] = [sheet for sheet in spec["sheets"] if sheet["name"] != "Sources"]
        self.assertIn("missing sheet: Sources", validate_pack.validate(spec))

    def test_missing_register_column(self):
        spec = valid_spec()
        register = spec["sheets"][1]
        register["headers"] = [h for h in register["headers"] if h != "How to obtain"]
        register["rows"] = [row[:4] + row[5:] for row in register["rows"]]
        self.assertTrue(any("missing the column: How to obtain" in issue
                            for issue in validate_pack.validate(spec)))

    def test_input_columns_must_come_last(self):
        spec = valid_spec()
        register = spec["sheets"][1]
        register["headers"] = register["headers"][:9] + ["Answer", "Status", "Evidence link", "Confidence"]
        self.assertTrue(any("must end with the columns" in issue for issue in validate_pack.validate(spec)))

    def test_question_with_no_owner(self):
        spec = valid_spec()
        spec["sheets"][1]["rows"][0][5] = ""
        self.assertIn("Q001: empty Who owns the answer", validate_pack.validate(spec))

    def test_question_with_no_hld_section(self):
        spec = valid_spec()
        spec["sheets"][1]["rows"][0][3] = "  "
        self.assertIn("Q001: empty Why it matters (HLD section)", validate_pack.validate(spec))

    def test_bad_priority(self):
        spec = valid_spec()
        spec["sheets"][1]["rows"][0][6] = "Critical"
        self.assertTrue(any("priority is 'Critical'" in issue for issue in validate_pack.validate(spec)))

    def test_undefined_workshop(self):
        spec = valid_spec()
        spec["sheets"][1]["rows"][0][7] = "W9"
        self.assertIn("Q001: workshop W9 is not defined on the Workshops sheet", validate_pack.validate(spec))

    def test_malformed_workshop_reference(self):
        spec = valid_spec()
        spec["sheets"][1]["rows"][0][7] = "workshop one"
        self.assertTrue(any("is not in the form W1" in issue for issue in validate_pack.validate(spec)))

    def test_duplicate_question_id(self):
        spec = valid_spec()
        spec["sheets"][1]["rows"][1][0] = spec["sheets"][1]["rows"][0][0]
        self.assertTrue(any("duplicate question ID" in issue for issue in validate_pack.validate(spec)))

    def test_too_few_questions(self):
        spec = valid_spec()
        spec["sheets"][1]["rows"] = spec["sheets"][1]["rows"][:10]
        self.assertTrue(any("only 10 questions" in issue for issue in validate_pack.validate(spec)))

    def test_too_few_domains(self):
        spec = valid_spec()
        for row in spec["sheets"][1]["rows"]:
            row[1] = "One domain"
        issues = validate_pack.validate(spec)
        self.assertTrue(any("only 1 domains" in issue for issue in issues))

    def test_domain_not_counted_on_the_dashboard(self):
        spec = valid_spec()
        spec["sheets"][5]["rows"] = spec["sheets"][5]["rows"][:-1]
        self.assertTrue(any("Dashboard does not count the domain" in issue
                            for issue in validate_pack.validate(spec)))

    def test_source_without_a_date(self):
        spec = valid_spec()
        spec["sheets"][4]["rows"][0][2] = "recently"
        self.assertTrue(any("no publication or update date" in issue
                            for issue in validate_pack.validate(spec)))

    def test_source_without_an_access_date(self):
        spec = valid_spec()
        spec["sheets"][4]["rows"][0][3] = ""
        self.assertTrue(any("no access date" in issue for issue in validate_pack.validate(spec)))

    def test_too_few_sources(self):
        spec = valid_spec()
        spec["sheets"][4]["rows"] = spec["sheets"][4]["rows"][:2]
        self.assertTrue(any("only 2 sources" in issue for issue in validate_pack.validate(spec)))

    def test_unreplaced_placeholder(self):
        spec = valid_spec()
        spec["sheets"][1]["rows"][0][2] = "{{question}}"
        self.assertIn("spec contains an unreplaced placeholder", validate_pack.validate(spec))

    def test_original_spec_is_not_mutated_by_validation(self):
        spec = valid_spec()
        before = copy.deepcopy(spec)
        validate_pack.validate(spec)
        self.assertEqual(spec, before)

class CommandLineTest(unittest.TestCase):
    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / "validate_pack.py"), *args],
                              capture_output=True, text=True)

    def test_usage_error(self):
        self.assertEqual(self.run_script().returncode, 2)

    def test_unreadable_spec(self):
        self.assertEqual(self.run_script("does-not-exist.json").returncode, 2)

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "spec.json"
            path.write_text("{not json", encoding="utf-8")
            self.assertEqual(self.run_script(str(path)).returncode, 2)

    def test_exit_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            good = Path(directory) / "good.json"
            good.write_text(json.dumps(valid_spec()), encoding="utf-8")
            self.assertEqual(self.run_script(str(good)).returncode, 0)
            spec = valid_spec()
            spec["sheets"][1]["rows"][0][5] = ""
            bad = Path(directory) / "bad.json"
            bad.write_text(json.dumps(spec), encoding="utf-8")
            result = self.run_script(str(bad))
            self.assertEqual(result.returncode, 1)
            self.assertIn("empty Who owns the answer", result.stdout)

if __name__ == '__main__':
    unittest.main()
