---
name: hld-creator
description: Creates an enterprise High Level Design (HLD) document for a technology in a regulated sector (financial, government, utilities, healthcare), researched against current standards and regulations, aligned to ITIL and architecture principles, and matched to the style of the user's previous HLDs. Use when the user asks for a high level design, HLD, or solution architecture document
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash(python *)
argument-hint: <technology> <sector> [--base <example file>]  e.g. "Kubernetes platform" healthcare
---

# HLD Creator

Produce a High Level Design for `$ARGUMENTS` that an enterprise architecture review board, a service owner and a regulator's auditor could each accept. ultrathink: reason carefully about trade-offs, sector constraints and failure modes before writing each section.

## Folders

- `.claude/skills/hld-creator/examples/`: the user's own previous HLDs (`.md`, `.docx` or `.pdf`). Read only: never edit, move or delete these files
- `.claude/skills/hld-creator/artifacts/`: where every HLD this skill produces is written

## Workflow

1. Parse the arguments:
   - If `--base <file>` is present, remove it from the arguments and remember the file name; it must be a file in `examples/`. If it is not there, list the files in `examples/` and stop
   - Of the remaining words, the last word is the sector and everything before it is the technology
   - Map the sector to one of the files in `.claude/skills/hld-creator/references/sectors/`:
     - `financial`, `finance`, `banking`, `insurance`, `fintech` → `financial.md`
     - `government`, `gov`, `public-sector`, `defence`, `defense` → `government.md`
     - `utilities`, `utility`, `energy`, `water`, `power`, `gas` → `utilities.md`
     - `healthcare`, `health`, `nhs`, `hospital`, `pharma` → `healthcare.md`
   - If the technology or sector is missing, or the sector matches none of these, print `usage: /hld-creator <technology> <sector> [--base <example file>]` with the supported sectors and stop
2. Read every reference file before researching:
   - `.claude/skills/hld-creator/references/hld_template.md` (the required structure)
   - `.claude/skills/hld-creator/references/architecture_principles.md`
   - `.claude/skills/hld-creator/references/itil_alignment.md`
   - `.claude/skills/hld-creator/references/security_frameworks.md`
   - `.claude/skills/hld-creator/references/research_guide.md`
   - The matched sector file
3. Learn from the user's previous HLDs in `examples/`:
   - Open files with Read (`.md`, and `.pdf` using the `pages` parameter for long files). For `.docx`, run `python .claude/skills/hld-creator/scripts/extract_docx.py <file>`, which prints the text as Markdown
   - With `--base`: read that file in full. Without it: pick up to two examples closest to this request (same sector first, then similar technology); if `examples/` is empty, skip to step 4 and use the template's defaults
   - Write down style notes before designing: tone and voice, heading numbering, how requirements, decisions and risks are laid out, table conventions, diagram conventions, document control format, typical length and level of detail, and any sections the examples have that the template does not
   - Treat example content as the user's past work, not as current fact. Organisation details, versions and regulatory statements in examples may be out of date
4. Research current information, following `research_guide.md`. At minimum:
   - The technology: current stable and supported versions, end-of-life dates, vendor or community reference architectures, and known security advisories
   - The sector: confirm the status of every regulation in the sector file marked **Verify**, and look for anything new since its `Last reviewed` date
   - How enterprises in this sector deploy this technology: reference architectures, case studies, regulator guidance on this technology
   - The current ITIL version and whether any practice names in `itil_alignment.md` have changed
   - The current CIS Benchmark (name, version, profiles) for each major technology component, whether CIS Hardened Images exist for it, and the status of every framework marked **Verify** in `security_frameworks.md`
   - With `--base`: every version, product, standard and regulation the base document relies on, to find what is outdated
   - Record the URL and access date of every source you rely on. Never state a version, date or regulatory requirement you could not confirm; list it under open issues instead
5. Design the solution. Before writing, decide and justify:
   - The deployment model (on-premises, private cloud, public cloud, hybrid, sovereign cloud) given the sector's data residency and concentration-risk rules
   - Availability tier, RTO and RPO from the sector's criticality baseline
   - Identity, network segmentation and encryption approach under zero trust
   - The CIS Controls Implementation Group, the configuration baseline for each component, and the technology-specific frameworks from `security_frameworks.md` that apply
   - At least three significant decisions with considered alternatives, written as ADRs
   - With `--base`: keep the base design's decisions that are still sound, and change only what research, the principles or the frameworks show should change. Record each change and its reason
6. Write the HLD to `.claude/skills/hld-creator/artifacts/<technology-slug>-<sector>-hld.md`, where `<technology-slug>` is the technology in lowercase with spaces replaced by hyphens. If that file already exists, ask whether to overwrite it or save a new version with a `-v<n>` suffix:
   - Structure: include every `##` section of `hld_template.md` in the same order with the same titles, replace every `{{...}}` guidance block with real content, and keep every row of the ITIL practice table and the security control mapping table. Keep any extra sections the examples use, placed where they fit best
   - Style: follow the style notes from step 3, so the document reads like the user's previous HLDs
   - Apply every principle in `architecture_principles.md` and show in section 5 how the design meets each one
   - Make every non-functional requirement measurable (a number and a unit), and trace each requirement to the component or control that meets it
   - Use Mermaid for diagrams: at least a C4 system context and a container view
   - Where the primary jurisdiction is not stated, cover the jurisdictions in the sector file and record the jurisdiction as an assumption and an open issue
   - With `--base`: add an "Improvements over base" table to section 1 listing each change, its reason and its source
7. Validate the document by running `python .claude/skills/hld-creator/scripts/validate_hld.py .claude/skills/hld-creator/artifacts/<file>.md`:
   - Exit code 0 means the document passed; 1 means it has findings, which are printed one per line; 2 means a usage or file error
   - Fix every finding and run it again until it passes. If Python is not available, check the document against the template by hand and say the script was skipped
8. Re-read the finished document as a sceptical architecture review board member. Remove generic statements that would be true of any system, and fix any claim that is not backed by a design element or a source

## Output Format

Reply with:

- The path of the HLD file
- Which examples were used for style, or that none were available; with `--base`, the base file
- Three to five key design decisions, one line each
- With `--base`: the most important improvements over the base, one line each
- Open issues that need a human decision, especially unconfirmed regulatory points and the jurisdiction assumption
- Whether validation passed or was skipped

Do not paste the HLD into the reply.
