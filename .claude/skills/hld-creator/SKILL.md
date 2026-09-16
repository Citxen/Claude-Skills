---
name: hld-creator
description: Creates an enterprise High Level Design (HLD) document for a technology in a regulated sector (financial, government, utilities, healthcare), researched against current standards and regulations and aligned to ITIL and architecture principles. Use when the user asks for a high level design, HLD, or solution architecture document
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash(python *)
argument-hint: <technology> <sector>  e.g. "Kubernetes platform" healthcare
---

# HLD Creator

Produce a High Level Design for `$ARGUMENTS` that an enterprise architecture review board, a service owner and a regulator's auditor could each accept. ultrathink: reason carefully about trade-offs, sector constraints and failure modes before writing each section.

## Workflow

1. Parse the arguments:
   - The last word is the sector; everything before it is the technology
   - Map the sector to one of the files in `.claude/skills/hld-creator/references/sectors/`:
     - `financial`, `finance`, `banking`, `insurance`, `fintech` → `financial.md`
     - `government`, `gov`, `public-sector`, `defence`, `defense` → `government.md`
     - `utilities`, `utility`, `energy`, `water`, `power`, `gas` → `utilities.md`
     - `healthcare`, `health`, `nhs`, `hospital`, `pharma` → `healthcare.md`
   - If the technology or sector is missing, or the sector matches none of these, print `usage: /hld-creator <technology> <sector>` with the supported sectors and stop
2. Read every reference file before researching:
   - `.claude/skills/hld-creator/references/hld_template.md` (the required structure)
   - `.claude/skills/hld-creator/references/architecture_principles.md`
   - `.claude/skills/hld-creator/references/itil_alignment.md`
   - `.claude/skills/hld-creator/references/security_frameworks.md`
   - `.claude/skills/hld-creator/references/research_guide.md`
   - The matched sector file
3. Research current information, following `research_guide.md`. At minimum:
   - The technology: current stable and supported versions, end-of-life dates, vendor or community reference architectures, and known security advisories
   - The sector: confirm the status of every regulation in the sector file marked **Verify**, and look for anything new since its `Last reviewed` date
   - How enterprises in this sector deploy this technology: reference architectures, case studies, regulator guidance on this technology
   - The current ITIL version and whether any practice names in `itil_alignment.md` have changed
   - The current CIS Benchmark (name, version, profiles) for each major technology component, whether CIS Hardened Images exist for it, and the status of every framework marked **Verify** in `security_frameworks.md`
   - Record the URL and access date of every source you rely on. Never state a version, date or regulatory requirement you could not confirm; list it under open issues instead
4. Design the solution. Before writing, decide and justify:
   - The deployment model (on-premises, private cloud, public cloud, hybrid, sovereign cloud) given the sector's data residency and concentration-risk rules
   - Availability tier, RTO and RPO from the sector's criticality baseline
   - Identity, network segmentation and encryption approach under zero trust
   - The CIS Controls Implementation Group, the configuration baseline for each component, and the technology-specific frameworks from `security_frameworks.md` that apply
   - At least three significant decisions with considered alternatives, written as ADRs
5. Write the HLD to `docs/hld/<technology-slug>-<sector>-hld.md`, where `<technology-slug>` is the technology in lowercase with spaces replaced by hyphens:
   - Follow `hld_template.md` exactly: keep every `##` section in the same order, replace every `{{...}}` guidance block with real content, and keep every row of the ITIL practice table and the security control mapping table
   - Apply every principle in `architecture_principles.md` and show in section 5 how the design meets each one
   - Make every non-functional requirement measurable (a number and a unit), and trace each requirement to the component or control that meets it
   - Use Mermaid for diagrams: at least a C4 system context and a container view
   - Where the primary jurisdiction is not stated, cover the jurisdictions in the sector file and record the jurisdiction as an assumption and an open issue
6. Validate the document by running `python .claude/skills/hld-creator/scripts/validate_hld.py docs/hld/<file>.md`:
   - Exit code 0 means the document passed; 1 means it has findings, which are printed one per line; 2 means a usage or file error
   - Fix every finding and run it again until it passes. If Python is not available, check the document against the template by hand and say the script was skipped
7. Re-read the finished document as a sceptical architecture review board member. Remove generic statements that would be true of any system, and fix any claim that is not backed by a design element or a source

## Output Format

Reply with:

- The path of the HLD file
- Three to five key design decisions, one line each
- Open issues that need a human decision, especially unconfirmed regulatory points and the jurisdiction assumption
- Whether validation passed or was skipped

Do not paste the HLD into the reply.
