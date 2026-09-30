import sys
import zipfile
import xml.etree.ElementTree as ET

M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
PR = "{http://schemas.openxmlformats.org/package/2006/relationships}"
DR = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

def column_index(reference):
    # "AB12" -> 27. Letters only; a cell with no reference falls back to the next free column
    index = 0
    for character in reference:
        if not character.isalpha():
            break
        index = index * 26 + (ord(character.upper()) - ord("A") + 1)
    return index - 1

def shared_strings(archive):
    try:
        root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return ["".join(node.text or "" for node in item.iter(f"{M}t")) for item in root.iter(f"{M}si")]

def sheet_paths(archive):
    # Yield (sheet name, part path) in workbook order
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {node.get("Id"): node.get("Target") for node in relationships.iter(f"{PR}Relationship")}
    for sheet in workbook.iter(f"{M}sheet"):
        target = targets.get(sheet.get(f"{DR}id"), "")
        if target:
            yield sheet.get("name", ""), "xl/" + target.lstrip("/").removeprefix("xl/")

def cell_text(cell, shared):
    if cell.get("t") == "inlineStr":
        return "".join(node.text or "" for node in cell.iter(f"{M}t"))
    value = cell.find(f"{M}v")
    if value is None or value.text is None:
        # A formula written without a cached result (what openpyxl produces, sometimes as an
        # empty <v/>) shows as the formula rather than as a blank cell
        formula = cell.find(f"{M}f")
        return "=" + (formula.text or "") if formula is not None else ""
    if cell.get("t") == "s":
        try:
            return shared[int(value.text)]
        except (ValueError, IndexError, TypeError):
            return ""
    return value.text or ""

def clean(text):
    return text.replace("|", "\\|").replace("\n", " ").strip()

def sheet_markdown(xml, shared):
    rows = []
    for row in ET.fromstring(xml).iter(f"{M}row"):
        cells, next_index = {}, 0
        for cell in row.iter(f"{M}c"):
            reference = cell.get("r") or ""
            index = column_index(reference) if reference[:1].isalpha() else next_index
            next_index = index + 1
            text = clean(cell_text(cell, shared))
            if text:
                cells[index] = text
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    width = max(max(cells) for cells in rows) + 1
    lines = ["| " + " | ".join(cells.get(i, "") for i in range(width)) + " |" for cells in rows]
    lines.insert(1, "|" + "---|" * width)
    return "\n".join(lines)

def extract(path, only=None):
    blocks = []
    with zipfile.ZipFile(path) as archive:
        shared = shared_strings(archive)
        for name, part in sheet_paths(archive):
            if only and name.lower() != only.lower():
                continue
            table = sheet_markdown(archive.read(part), shared)
            blocks.append(f"## {name}\n\n{table}" if table else f"## {name}\n\n(empty)")
    return "\n\n".join(blocks)

if __name__ == '__main__':
    if not 2 <= len(sys.argv) <= 3:
        print("usage: extract_xlsx.py <file.xlsx> [sheet name]", file=sys.stderr)
        sys.exit(2)
    try:
        text = extract(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None)
    except (OSError, KeyError, zipfile.BadZipFile, ET.ParseError) as e:
        print(f"error: cannot read {sys.argv[1]}: {e}", file=sys.stderr)
        sys.exit(1)
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)
