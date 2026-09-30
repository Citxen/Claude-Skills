# Workbook Specification Reference

`scripts/build_workbook.py` turns a JSON specification into the workbook. The spec carries the
content; the script owns the formatting, so every pack looks the same. `scripts/validate_pack.py`
reads the same JSON and must pass before the workbook is delivered.

## Required tabs, in this order

| Tab | Purpose |
|---|---|
| Read me | Purpose, how the pack is structured, which cells to fill in, currency warning, tab list |
| Discovery register | The master question list. One row per question |
| One tab per major inventory | Estate, applications, and whichever of the domains need a structured inventory rather than a question |
| Sector or environment tab | The feature-gap and assurance check, named for the sector (for example "Government") |
| Tooling | Every data-collection route: what it gathers, permissions needed, caveats, reference |
| Workshops | One row per session: attendees, duration, inputs, outputs, register rows closed |
| RAID and decisions | What discovery cannot close, and where each item lands in the HLD |
| Sources | Every source, with dates and the comment-section assessment |
| Dashboard | Progress counts by domain, as formulas over the register |

Aim for twelve to twenty tabs. Fewer than twelve usually means inventories have been collapsed
into questions; more than twenty means the register is being duplicated.

## Discovery register columns

These are fixed. `validate_pack.py` enforces the names, and that the four the reader completes
come last:

`ID`, `Domain`, `Question or data point`, `Why it matters (HLD section)`, `How to obtain`,
`Who owns the answer`, `Priority`, `Workshop`, an optional flag column whose name ends
`flag to confirm`, then `Answer`, `Evidence link`, `Status`, `Confidence`.

## Spec shape

```json
{
  "output": "C:/path/to/pack.xlsx",
  "sheets": [
    {
      "name": "Discovery register",
      "title": "Discovery register",
      "subtitle": "One row per question. Fill Answer, Evidence link, Status and Confidence.",
      "headers": ["ID", "Domain", "..."],
      "widths": [7, 22, 58],
      "rows": [["A01", "Objectives and scope", "..."]],
      "freeze": "A5",
      "filter": true,
      "input_columns": ["J", "K", "L", "M"],
      "dropdowns": {"L": ["Open", "In progress", "Answered", "Blocked", "Not applicable"]},
      "flag_column": 9,
      "flag_prefix": "GOV GAP",
      "example_rows": [1]
    }
  ]
}
```

- `headers` and `widths` are positional and must be the same length as each row.
- `rows` values are written as they are; a string starting with `=` becomes a formula.
- `input_columns` shades the columns the reader completes.
- `dropdowns` maps a column letter to its allowed values.
- `flag_column` is 1-based; any row whose cell in that column starts with `flag_prefix`
  (default `GOV GAP`) is shaded, so limitations are visible without reading.
- `example_rows` is 1-based over `rows`; those rows render grey italic as worked examples.
- The title is row 1, the subtitle row 2, headers row 4, and data from row 5. Formula ranges that
  point at the register therefore start at row 5.

## Formulas

The Dashboard counts by domain with `COUNTIF` and `COUNTIFS` over the register. Use only
functions that any spreadsheet application evaluates; avoid `XLOOKUP`, `FILTER`, `UNIQUE` and the
other spilling array functions.

openpyxl writes formulas without a cached result, so the Dashboard reads as blank until the
workbook is opened in a spreadsheet application, which recalculates on open. Say so on the
Dashboard itself and in the reply, rather than leaving the reader thinking it is broken.

## Inventory tabs

Every inventory tab carries one worked example row, marked in `example_rows`, showing the
expected format with invented values, and its subtitle tells the reader to delete it. Never use a
real organisation's data in an example.

## Companion document

Alongside the workbook, write a Markdown method document to the same folder: purpose, principles,
phases, how to run the workshops, the evidence checklist, tooling and access rules, the feature-gap
check, the source assessment, and what completion looks like. It explains how to run the pack; the
workbook holds the content.
