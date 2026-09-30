---
name: discovery-creator
description: Creates an information-gathering pack - an Excel discovery workbook and a method document - for a technology in a regulated sector (financial, government, utilities, healthcare), so the answers needed to write a High Level Design can be collected before any design starts. Researched against current vendor documentation and practitioner sources. Use when the user asks for discovery, an assessment, a questionnaire, a requirements-gathering pack or a current-state review
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash(python *)
argument-hint: <technology> <sector> [--refresh <pack file>]  e.g. "Microsoft Intune" government
---

# Discovery Creator

Produce the pack that gathers what a High Level Design for `$ARGUMENTS` needs. ultrathink: work out what the design will actually have to decide, and ask only the questions that settle those decisions.

This pack gathers information. It contains no design decisions, no recommendations and no solution content. If a question forces a decision, it belongs on the RAID tab, not in an answer.

## Folders

- `.claude/skills/hld-creator/references/`: shared reference material. The sector files, the HLD template and the architecture principles live there and are not duplicated here. Read only
- `.claude/skills/hld-creator/artifacts/discovery/`: where every pack this skill produces is written. The `hld-creator` skill reads this folder as input, which is how discovery reaches the design

## Workflow

1. Parse the arguments:
   - If `--refresh <file>` is present, remove it from the arguments and remember the file name; it must be a file in `.claude/skills/hld-creator/artifacts/discovery/`. If it is not there, list that folder and stop. Then follow **Refresh mode** below
   - Of the remaining words, the last word is the sector and everything before it is the technology
   - Map the sector to one of the files in `.claude/skills/hld-creator/references/sectors/`:
     - `financial`, `finance`, `banking`, `insurance`, `fintech` → `financial.md`
     - `government`, `gov`, `public-sector`, `defence`, `defense` → `government.md`
     - `utilities`, `utility`, `energy`, `water`, `power`, `gas` → `utilities.md`
     - `healthcare`, `health`, `nhs`, `hospital`, `pharma` → `healthcare.md`
   - If the technology or sector is missing, or the sector matches none of these, print `usage: /discovery-creator <technology> <sector> [--refresh <pack file>]` with the supported sectors and stop
2. Read every reference file before researching:
   - `.claude/skills/discovery-creator/references/discovery_domains.md` (the seventeen domains and what each must establish)
   - `.claude/skills/discovery-creator/references/workbook_spec.md` (the tabs, the register columns and the spec the builder takes)
   - `.claude/skills/discovery-creator/references/research_guide.md`
   - `.claude/skills/hld-creator/references/hld_template.md`, so every question can name the section it feeds
   - The matched sector file
3. Research, following `research_guide.md`. At minimum:
   - The vendor's current planning, deployment and migration guidance for this technology
   - How the technology differs in the deployment the sector demands - a government or sovereign cloud, a restricted region, an air-gapped build. Build the feature-gap list from the vendor's own service description, not from a summary of it
   - The network, licensing and identity prerequisites a reader will have to check
   - Vendor-published readiness reports, assessment tools and planning templates
   - Practitioner and MVP sources for inventory and audit method, especially for the migration source
   - The tools that actually gather each kind of data, their permissions and their caveats, including whether each is maintained
   - For each obligation in the sector file marked **Verify**, its current status
   - Assess the comments on every community source and record the outcome, using the wording in `research_guide.md`
4. Compose the content before building anything:
   - Work domain by domain through `discovery_domains.md`. For each, write the questions that this technology in this sector actually requires
   - Give every question: how to obtain it, the role that owns it, a priority, a workshop, and the HLD section it feeds
   - Identify the audit periods that must start in week one, and say so in the pack
   - Build the feature-gap list, one row per capability, with the source checked and the date checked
   - Design the workshops so that every register row is closed by exactly one of them, and order them so a session that needs another session's output comes later
   - Expect 120 to 200 questions. Materially fewer means the estate, the applications or the regulatory domain has been skimmed
5. Write the specification as JSON to `.claude/skills/hld-creator/artifacts/discovery/<technology-slug>-<sector>-discovery-spec.json`, where `<technology-slug>` is the technology in lowercase with spaces replaced by hyphens, following `workbook_spec.md`. Keep the spec: it is how the pack is refreshed later
6. Validate the spec with `python .claude/skills/discovery-creator/scripts/validate_pack.py <spec>.json`:
   - Exit code 0 means it passed; 1 means findings, printed one per line; 2 means a usage or file error
   - Fix every finding and run it again until it passes
7. Build the workbook with `python .claude/skills/discovery-creator/scripts/build_workbook.py <spec>.json`, which writes the `output` path in the spec: `.claude/skills/hld-creator/artifacts/discovery/<technology-slug>-<sector>-discovery-pack.xlsx`. If that file already exists, ask whether to overwrite it or save a new version with a `-v<n>` suffix
   - If openpyxl is missing the script exits 2 and says so. Install it with `python -m pip install openpyxl`, or, if that is not possible, deliver the spec and the method document and say the workbook was not built
8. Write the companion method document to `.claude/skills/hld-creator/artifacts/discovery/<technology-slug>-<sector>-discovery-method.md`, covering purpose, principles, phases, how to run the workshops, the evidence checklist, tooling and access, the feature-gap check, the source assessment, and what completion looks like
9. Re-read the pack as the person who has to fill it in. Remove any question that no HLD section needs, any question whose answer you could have looked up yourself, and any instruction to "investigate" that names no source. Confirm every example row is invented

## Refresh mode

With `--refresh <file>`, update an existing pack rather than writing a new one. Do steps 1 and 2, then:

1. Read the pack's saved spec if it exists beside the file, and the pack itself. Read an `.xlsx` with `python .claude/skills/hld-creator/scripts/extract_xlsx.py <file>`
2. Re-run the research in step 3, comparing against the Sources tab: what has changed since each access date, what has moved between a vendor's supported, planned and unavailable lists, what has been archived or deprecated
3. Update the affected rows, the feature-gap tab and the Sources tab, leaving every answer the user has already recorded untouched. Never clear a filled-in cell
4. Validate and rebuild as in steps 6 and 7
5. Reply with what changed, one line each, and what the change means for anyone already relying on the old pack

## Output Format

Reply with:

- The paths of the workbook, the method document and the spec
- The sector reference file used
- The question count, the domain count and the workshop count
- The feature gaps found, one line each, or that none apply to this technology and sector
- Anything the research could not confirm, and what the reader must check
- The decisions the pack will force, especially jurisdiction and deployment environment
- Whether validation passed, and whether the workbook was built
- The command that turns the completed pack into an HLD: `/hld-creator <technology> <sector> --skeleton` first, then the full run

Do not paste the register into the reply.
