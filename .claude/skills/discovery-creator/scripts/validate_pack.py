"""Check a discovery pack specification before it is built.

Reads the same JSON that build_workbook.py consumes and reports anything that would make the
pack unusable: a question nobody owns, a question that feeds no HLD section, a workshop
reference that does not exist, a source with no date. Standard library only.
"""
import json
import re
import sys
from pathlib import Path

REQUIRED_SHEETS = ["Read me", "Discovery register", "Tooling", "Workshops", "Sources", "Dashboard"]
REQUIRED_REGISTER_COLUMNS = ["ID", "Domain", "Question or data point", "Why it matters (HLD section)",
                             "How to obtain", "Who owns the answer", "Priority", "Workshop"]
TRAILING_REGISTER_COLUMNS = ["Answer", "Evidence link", "Status", "Confidence"]
PRIORITIES = {"Must", "Should", "Could"}
MIN_QUESTIONS = 60
MIN_DOMAINS = 8
MIN_SOURCES = 5
YEAR = re.compile(r"(19|20)\d{2}")
WORKSHOP_REF = re.compile(r"^W\d+$")

def sheets_by_name(spec):
    return {sheet.get("name", ""): sheet for sheet in spec.get("sheets") or []}

def column(sheet, name):
    headers = sheet.get("headers") or []
    return headers.index(name) if name in headers else None

def cell(row, index):
    return str(row[index]).strip() if index is not None and index < len(row) and row[index] is not None else ""

def check_sheets(sheets):
    return [f"missing sheet: {name}" for name in REQUIRED_SHEETS if name not in sheets]

def check_register(sheets):
    issues = []
    register = sheets.get("Discovery register")
    if register is None:
        return issues
    headers = register.get("headers") or []
    for name in REQUIRED_REGISTER_COLUMNS + TRAILING_REGISTER_COLUMNS:
        if name not in headers:
            issues.append(f"Discovery register is missing the column: {name}")
    if headers[-4:] != TRAILING_REGISTER_COLUMNS:
        issues.append("Discovery register must end with the columns the reader fills in: "
                      + ", ".join(TRAILING_REGISTER_COLUMNS))

    indexes = {name: column(register, name) for name in REQUIRED_REGISTER_COLUMNS}
    workshops = workshop_refs(sheets)
    rows = register.get("rows") or []
    if len(rows) < MIN_QUESTIONS:
        issues.append(f"only {len(rows)} questions (expected at least {MIN_QUESTIONS})")

    seen, domains = set(), set()
    for number, row in enumerate(rows, start=1):
        identifier = cell(row, indexes["ID"]) or f"row {number}"
        if identifier in seen:
            issues.append(f"duplicate question ID: {identifier}")
        seen.add(identifier)
        domains.add(cell(row, indexes["Domain"]))
        for name in ("Domain", "Question or data point", "Why it matters (HLD section)",
                     "How to obtain", "Who owns the answer"):
            if not cell(row, indexes[name]):
                issues.append(f"{identifier}: empty {name}")
        priority = cell(row, indexes["Priority"])
        if priority not in PRIORITIES:
            issues.append(f"{identifier}: priority is '{priority}', expected one of {', '.join(sorted(PRIORITIES))}")
        workshop = cell(row, indexes["Workshop"])
        if not WORKSHOP_REF.match(workshop):
            issues.append(f"{identifier}: workshop reference '{workshop}' is not in the form W1")
        elif workshops and workshop not in workshops:
            issues.append(f"{identifier}: workshop {workshop} is not defined on the Workshops sheet")
    if len(domains) < MIN_DOMAINS:
        issues.append(f"only {len(domains)} domains (expected at least {MIN_DOMAINS})")
    return issues

def workshop_refs(sheets):
    workshops = sheets.get("Workshops")
    if workshops is None:
        return set()
    return {str(row[0]).strip() for row in (workshops.get("rows") or []) if row}

def check_dashboard(sheets):
    register, dashboard = sheets.get("Discovery register"), sheets.get("Dashboard")
    if register is None or dashboard is None:
        return []
    index = column(register, "Domain")
    counted = {str(row[0]).strip() for row in (dashboard.get("rows") or []) if row}
    missing = sorted({cell(row, index) for row in (register.get("rows") or [])} - counted)
    return [f"Dashboard does not count the domain: {domain}" for domain in missing if domain]

def check_sources(sheets):
    issues = []
    sources = sheets.get("Sources")
    if sources is None:
        return issues
    rows = sources.get("rows") or []
    if len(rows) < MIN_SOURCES:
        issues.append(f"only {len(rows)} sources (expected at least {MIN_SOURCES})")
    published, accessed = column(sources, "Published or updated"), column(sources, "Accessed")
    if published is None or accessed is None:
        issues.append("Sources needs both a 'Published or updated' and an 'Accessed' column")
        return issues
    for number, row in enumerate(rows, start=1):
        label = cell(row, 0) or f"row {number}"
        if not YEAR.search(cell(row, published)):
            issues.append(f"source {label}: no publication or update date")
        if not YEAR.search(cell(row, accessed)):
            issues.append(f"source {label}: no access date")
    return issues

def check_placeholders(spec):
    text = json.dumps(spec)
    return ["spec contains an unreplaced placeholder"] if "{{" in text or "}}" in text else []

def validate(spec):
    sheets = sheets_by_name(spec)
    return (check_sheets(sheets) + check_register(sheets) + check_dashboard(sheets)
            + check_sources(sheets) + check_placeholders(spec))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: validate_pack.py <spec.json>", file=sys.stderr)
        sys.exit(2)
    try:
        specification = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"error: cannot read spec: {error}", file=sys.stderr)
        sys.exit(2)
    findings = validate(specification)
    for finding in findings:
        print(finding)
    sys.exit(1 if findings else 0)
