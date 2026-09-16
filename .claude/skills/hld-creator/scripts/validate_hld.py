import re
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "references" / "hld_template.md"
HEADING = re.compile(r"^##\s+(?:\d+\.\s+)?(.+?)\s*$")
# Sections whose table rows (first column) must all appear in the HLD, with the name used in findings
REQUIRED_TABLES = {
    "Service Management (ITIL) Alignment": "ITIL table missing practice",
    "Security Architecture": "security control mapping missing function",
}
SECURITY_SECTION = "Security Architecture"
SECURITY_TERMS = ["CIS Controls", "Implementation Group", "CIS Benchmark"]
REFERENCES_SECTION = "References"
MIN_DIAGRAMS = 2
MIN_REFERENCES = 5

def parse_sections(text):
    # Return [(title, line_number, body_lines)] for each "## " heading, ignoring headings inside code blocks
    sections, in_code = [], False
    for number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
        match = None if in_code else HEADING.match(line)
        if match:
            sections.append((match.group(1), number, []))
        elif sections:
            sections[-1][2].append(line)
    return sections

def table_first_cells(lines):
    cells = []
    for line in lines:
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if line.strip().startswith("|") and parts[0] and not set(parts[0]) <= set("-: "):
            cells.append(parts[0])
    return cells[1:]  # drop the header row

def check_structure(required, sections):
    issues = []
    found = [title.lower() for title, _, _ in sections]
    positions = []
    for title in required:
        if title.lower() not in found:
            issues.append(f"missing section: {title}")
        else:
            positions.append((found.index(title.lower()), title))
    for (previous, _), (current, title) in zip(positions, positions[1:]):
        if current < previous:
            issues.append(f"section out of order: {title}")
    for title, number, body in sections:
        if not any(line.strip() for line in body):
            issues.append(f"{number}: empty section: {title}")
    return issues

def check_content(text, sections):
    issues = []
    for number, line in enumerate(text.splitlines(), start=1):
        if "{{" in line or "}}" in line:
            issues.append(f"{number}: unreplaced template placeholder")
    diagrams = len(re.findall(r"^\s*```mermaid", text, flags=re.MULTILINE))
    if diagrams < MIN_DIAGRAMS:
        issues.append(f"only {diagrams} Mermaid diagrams (need at least {MIN_DIAGRAMS})")
    bodies = {title.lower(): "\n".join(body) for title, _, body in sections}
    security = bodies.get(SECURITY_SECTION.lower(), "").lower()
    for term in SECURITY_TERMS:
        if term.lower() not in security:
            issues.append(f"{SECURITY_SECTION} does not mention: {term}")
    links = re.findall(r"https?://", bodies.get(REFERENCES_SECTION.lower(), ""))
    if len(links) < MIN_REFERENCES:
        issues.append(f"only {len(links)} links in References (need at least {MIN_REFERENCES})")
    return issues

def check_tables(template_sections, sections):
    issues = []
    template_bodies = {title: body for title, _, body in template_sections}
    bodies = {title.lower(): body for title, _, body in sections}
    for section, message in REQUIRED_TABLES.items():
        rows = {cell.lower() for cell in table_first_cells(bodies.get(section.lower(), []))}
        for row in table_first_cells(template_bodies.get(section, [])):
            if row.lower() not in rows:
                issues.append(f"{message}: {row}")
    return issues

def validate(hld_text, template_text):
    template_sections = parse_sections(template_text)
    required = [title for title, _, _ in template_sections]
    sections = parse_sections(hld_text)
    return (check_structure(required, sections) + check_tables(template_sections, sections)
            + check_content(hld_text, sections))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: validate_hld.py <hld.md>", file=sys.stderr)
        sys.exit(2)
    try:
        hld_text = Path(sys.argv[1]).read_text(encoding="utf-8")
        template_text = TEMPLATE.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        sys.exit(2)
    issues = validate(hld_text, template_text)
    for issue in issues:
        print(issue)
    sys.exit(1 if issues else 0)
