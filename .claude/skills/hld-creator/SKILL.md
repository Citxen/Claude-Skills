---
name: hld-creator
description: Creates an enterprise High Level Design (HLD) document for a technology in a regulated sector (financial, government, utilities, healthcare), researched against current standards and regulations, aligned to ITIL and architecture principles, and matched to the style of the user's previous HLDs. Use when the user asks for a high level design, HLD, or solution architecture document
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash(python *)
argument-hint: <technology> <sector> [--base <example file>] [--skeleton]  e.g. "Kubernetes platform" healthcare
---

# HLD Creator

Produce a High Level Design for `$ARGUMENTS` that an enterprise architecture review board, a service owner and a regulator's auditor could each accept. ultrathink: reason carefully about trade-offs, sector constraints and failure modes before writing each section.

## Folders

- `.claude/skills/hld-creator/examples/`: the user's own previous HLDs (`.md`, `.docx` or `.pdf`). Read only: never edit, move or delete these files
- `.claude/skills/hld-creator/artifacts/`: where every HLD this skill produces is written
- `.claude/skills/hld-creator/artifacts/discovery/`: inputs gathered about the organisation before the design - discovery packs, filled-in questionnaires, inventories and workshop notes. Read only: never edit, move or delete these files

## Workflow

1. Parse the arguments:
   - If `--base <file>` is present, remove it from the arguments and remember the file name. Look for it in `examples/` and then in `artifacts/`. If it is in neither, list the files in both folders and stop. Then classify it:
     - A file in `artifacts/` whose name ends `-hld-skeleton.md` is a **skeleton base**: an agreed structure for this document, with no content to learn style or design from
     - Any other base is an **example base**: the user's earlier work, used for style and as a design baseline
   - If `--skeleton` is present anywhere in the arguments, remove it and remember it; once parsing is done, follow **Skeleton mode** below instead of steps 4 to 9
   - Of the remaining words, the last word is the sector and everything before it is the technology
   - Map the sector to one of the files in `.claude/skills/hld-creator/references/sectors/`:
     - `financial`, `finance`, `banking`, `insurance`, `fintech` → `financial.md`
     - `government`, `gov`, `public-sector`, `defence`, `defense` → `government.md`
     - `utilities`, `utility`, `energy`, `water`, `power`, `gas` → `utilities.md`
     - `healthcare`, `health`, `nhs`, `hospital`, `pharma` → `healthcare.md`
   - If the technology or sector is missing, or the sector matches none of these, print `usage: /hld-creator <technology> <sector> [--base <example file>] [--skeleton]` with the supported sectors and stop
2. Read every reference file before researching:
   - `.claude/skills/hld-creator/references/hld_template.md` (the required structure)
   - `.claude/skills/hld-creator/references/architecture_principles.md`
   - `.claude/skills/hld-creator/references/itil_alignment.md`
   - `.claude/skills/hld-creator/references/security_frameworks.md`
   - `.claude/skills/hld-creator/references/research_guide.md`
   - The matched sector file
3. Read the discovery inputs, if `.claude/skills/hld-creator/artifacts/discovery/` exists and holds files. These are the organisation's own answers, and they outrank the template's defaults and anything you would otherwise assume:
   - `.md` and `.txt` with Read; `.pdf` with Read using the `pages` parameter; `.docx` with `python .claude/skills/hld-creator/scripts/extract_docx.py <file>`; `.xlsx` with `python .claude/skills/hld-creator/scripts/extract_xlsx.py <file>`, which prints every sheet as a Markdown table, or `python .claude/skills/hld-creator/scripts/extract_xlsx.py <file> "<sheet name>"` for a single sheet
   - Write down what is answered, what is still open, and every point the pack flags as unconfirmed
   - A discovery answer is evidence about the organisation, not a design decision. It tells you what is true, not what the design should be
   - If the folder is missing or empty, say so in the reply and design from the template's defaults
4. Learn from the user's previous HLDs in `examples/`:
   - Open files with Read (`.md`, and `.pdf` using the `pages` parameter for long files). For `.docx`, run `python .claude/skills/hld-creator/scripts/extract_docx.py <file>`, which prints the text as Markdown
   - With an example base: read that file in full. With a skeleton base or no base: pick up to two examples closest to this request (same sector first, then similar technology); if `examples/` is empty, skip to step 5 and use the template's defaults
   - Write down style notes before designing: tone and voice, heading numbering, how requirements, decisions and risks are laid out, table conventions, diagram conventions, document control format, typical length and level of detail, and any sections the examples have that the template does not
   - Treat example content as the user's past work, not as current fact. Organisation details, versions and regulatory statements in examples may be out of date
5. Research current information, following `research_guide.md`. At minimum:
   - The technology: current stable and supported versions, end-of-life dates, vendor or community reference architectures, and known security advisories
   - The sector: confirm the status of every regulation in the sector file marked **Verify**, and look for anything new since its `Last reviewed` date
   - How enterprises in this sector deploy this technology: reference architectures, case studies, regulator guidance on this technology
   - The current ITIL version and whether any practice names in `itil_alignment.md` have changed
   - The current CIS Benchmark (name, version, profiles) for each major technology component, whether CIS Hardened Images exist for it, and the status of every framework marked **Verify** in `security_frameworks.md`
   - With an example base: every version, product, standard and regulation the base document relies on, to find what is outdated. A skeleton base asserts nothing, so there is nothing in it to check
   - Anything the discovery inputs record as unconfirmed, especially a cloud feature gap: confirm it against the vendor's current documentation rather than repeating the status the pack recorded
   - Record the URL and access date of every source you rely on. Never state a version, date or regulatory requirement you could not confirm; list it under open issues instead
6. Design the solution. Before writing, decide and justify:
   - The deployment model (on-premises, private cloud, public cloud, hybrid, sovereign cloud) given the sector's data residency and concentration-risk rules
   - Availability tier, RTO and RPO from the sector's criticality baseline
   - Identity, network segmentation and encryption approach under zero trust
   - The CIS Controls Implementation Group, the configuration baseline for each component, and the technology-specific frameworks from `security_frameworks.md` that apply
   - At least three significant decisions with considered alternatives, written as ADRs
   - Use the discovery answers in place of assumptions wherever they exist. Where discovery left a question open, carry it into section 17 as an assumption or open issue with its owner, rather than settling it silently
   - With an example base: keep the base design's decisions that are still sound, and change only what research, the principles or the frameworks show should change. Record each change and its reason
   - With a skeleton base: its subheadings are the agreed scope of each section, and its ADR subheadings name the decisions the user expects to see decided. Design those decisions, and raise any further decision the design needs as an extra ADR
7. Write the HLD to `.claude/skills/hld-creator/artifacts/<technology-slug>-<sector>-hld.md`, where `<technology-slug>` is the technology in lowercase with spaces replaced by hyphens. If that file already exists, ask whether to overwrite it or save a new version with a `-v<n>` suffix:
   - Structure: include every `##` section of `hld_template.md` in the same order with the same titles, replace every `{{...}}` guidance block with real content, and keep every row of the ITIL practice table and the security control mapping table. Keep any extra sections the examples use, placed where they fit best
   - Style: follow the style notes from step 4, so the document reads like the user's previous HLDs
   - Apply every principle in `architecture_principles.md` and show in section 5 how the design meets each one
   - Make every non-functional requirement measurable (a number and a unit), and trace each requirement to the component or control that meets it
   - Where a requirement, risk or open issue came from the discovery inputs, cite the row or section it came from, so a reviewer can follow it back to the evidence
   - Use Mermaid for diagrams: at least a C4 system context and a container view
   - Where the primary jurisdiction is not stated, cover the jurisdictions in the sector file and record the jurisdiction as an assumption and an open issue
   - With a skeleton base: follow its headings in its order, including any the user has added, renamed, reordered or removed, and write the content under each. Where it marks a table or a diagram, produce that table or diagram. If it is missing a `##` section of `hld_template.md`, add that section back, because the finished document is validated against the template, and say so in the reply
   - With an example base: add an "Improvements over base" table to section 1 listing each change, its reason and its source
8. Validate the document by running `python .claude/skills/hld-creator/scripts/validate_hld.py .claude/skills/hld-creator/artifacts/<file>.md`:
   - Exit code 0 means the document passed; 1 means it has findings, which are printed one per line; 2 means a usage or file error
   - Fix every finding and run it again until it passes. If Python is not available, check the document against the template by hand and say the script was skipped
9. Re-read the finished document as a sceptical architecture review board member. Remove generic statements that would be true of any system, and fix any claim that is not backed by a design element or a source

## Skeleton mode

With `--skeleton`, produce the framework of the document only: its section and subsection headings with no body content, so the user can agree the shape of the HLD before any of it is written. Do steps 1 and 2, then (skeleton mode does not read the discovery inputs in step 3):

1. Read structure sources only. `hld_template.md` gives the `##` sections. The matched sector file, `architecture_principles.md`, `itil_alignment.md` and `security_frameworks.md` give the topics that deserve their own subheading for this technology and sector. Do not research, do not design the solution, and do not open a base unless `--base` was given, in which case read it for its heading structure and numbering only. A skeleton base means the user is revising a structure already agreed: keep their edits and change only what they asked for
2. Write `.claude/skills/hld-creator/artifacts/<technology-slug>-<sector>-hld-skeleton.md`, following the same overwrite rule as step 7:
   - A `# High Level Design: <Technology> for <Sector>` title, then one italic line naming the document as a skeleton and giving the command that turns it into the full HLD, then every `##` section of `hld_template.md` in the same order with the same titles
   - Under each section, `###` subheadings for the topics that section must cover here. Make them specific: name the regulations, frameworks, ITIL practices, environments and components that actually apply to this technology and sector, rather than repeating the template's generic wording
   - Headings only. No paragraphs, no tables, no diagrams and no `{{...}}` placeholders. Where a section will hold a table or a diagram, put a one-line italic note under its subheading saying what it will contain, for example `*Table: interface ID, source, target, pattern, protocol, classification.*`
   - Keep any extra sections and heading conventions the base document uses
3. Validate with `python .claude/skills/hld-creator/scripts/validate_hld.py --skeleton .claude/skills/hld-creator/artifacts/<file>.md`, which checks the section structure and skips the checks a skeleton cannot meet. Fix every finding and run it again until it passes
4. Reply with the file path, the sector reference file used, the section and subheading counts, what the user should decide before the full HLD is written (the jurisdiction above all), and the command that produces the full document from the same arguments

## Output Format

Reply with:

- The path of the HLD file
- Which examples were used for style, or that none were available; with `--base`, the base file
- Which discovery inputs were read, or that the discovery folder was empty
- Three to five key design decisions, one line each
- With an example base: the most important improvements over the base, one line each
- With a skeleton base: any heading of theirs you could not keep, and any template section you had to add back
- Open issues that need a human decision, especially unconfirmed regulatory points and the jurisdiction assumption
- Whether validation passed or was skipped

With `--skeleton`, reply as step 4 of Skeleton mode says instead.

Do not paste the HLD into the reply.
