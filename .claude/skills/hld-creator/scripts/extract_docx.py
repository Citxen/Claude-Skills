import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
HEADING_STYLE = re.compile(r"^(?:Heading|Title)(\d?)$", re.IGNORECASE)

def paragraph_text(paragraph):
    return "".join(node.text or "" for node in paragraph.iter(f"{W}t")).strip()

def heading_level(paragraph):
    style = paragraph.find(f"{W}pPr/{W}pStyle")
    match = HEADING_STYLE.match(style.get(f"{W}val", "")) if style is not None else None
    if not match:
        return 0
    return int(match.group(1)) if match.group(1) else 1  # "Title" is treated as level 1

def table_markdown(table):
    rows = []
    for row in table.iter(f"{W}tr"):
        cells = [" ".join(paragraph_text(p) for p in cell.iter(f"{W}p")).replace("|", "\\|")
                 for cell in row.iter(f"{W}tc")]
        rows.append("| " + " | ".join(cells) + " |")
    if rows:
        rows.insert(1, "|" + "---|" * rows[0].count(" | ") + "---|")
    return "\n".join(rows)

def blocks(container):
    # Yield Markdown blocks in document order, including content inside content controls (w:sdt)
    for element in container:
        if element.tag == f"{W}tbl":
            yield table_markdown(element)
        elif element.tag == f"{W}p" and paragraph_text(element):
            level = heading_level(element)
            prefix = "#" * min(level, 6) + " " if level else ""
            yield prefix + paragraph_text(element)
        elif element.tag == f"{W}sdt" and element.find(f"{W}sdtContent") is not None:
            yield from blocks(element.find(f"{W}sdtContent"))

def extract(path):
    with zipfile.ZipFile(path) as archive:
        body = ET.fromstring(archive.read("word/document.xml")).find(f"{W}body")
    return "\n\n".join(blocks(body))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: extract_docx.py <file.docx>", file=sys.stderr)
        sys.exit(2)
    try:
        text = extract(sys.argv[1])
    except (OSError, KeyError, zipfile.BadZipFile, ET.ParseError) as e:
        print(f"error: cannot read {sys.argv[1]}: {e}", file=sys.stderr)
        sys.exit(1)
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)
