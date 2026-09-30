# Intune for Government: Discovery Method and Workshop Pack

*Companion to microsoft-intune-government-discovery-pack.xlsx. Prepared 30 September 2026, rebuilt through the discovery-creator skill the same day. This pack gathers the information a High Level Design needs; it contains no design decisions.*

## 1. Purpose and scope

This pack exists to answer one question: what do we need to know before anyone writes the High Level Design for Microsoft Intune in a government setting?

It is deliberately not a design. Every row in the workbook records a question, how to obtain the answer, who owns it, and which HLD section consumes it. When discovery closes, each row is either answered with evidence, or it becomes an assumption, an open issue or an architecture decision in the design.

The structure follows the seven steps of the Microsoft Intune planning guide, extended with the government, assurance, privacy, resilience and service-management areas that an enterprise architecture review board and a regulator's auditor will expect to see covered. It also mirrors the table set that Microsoft publishes in its **IDPDIG - Table templates** download, which covers deployment planning, current environment assessment, profiles, applications, compliance and validation.

## 2. Principles for running this discovery

- **Evidence over assertion.** An answer without a link to an export, a report or a named document is not an answer. The workbook has an Evidence link column for that reason.
- **Determine the goal, not the current configuration.** Microsoft's planning guide is explicit that twenty-year-old Group Policy Objects should not be carried forward simply because they exist. Capture what a setting is *for*, not only what it does.
- **Listen before you change.** For anything that removes a user capability, run an audit period first. The clearest example is local administrator rights: deploy an elevation policy in reporting-only mode for two to four weeks, see what people actually elevate, then map that to personas.
- **Confirm capability before you design with it.** In GCC High and DoD, a number of headline Intune capabilities are unavailable or restricted. Thirteen of these are flagged in the register. Each one must be confirmed against Microsoft's government service description on the day the design is written, not on the day this pack was built.
- **Separate discovery from decision.** Where a question forces a decision, it is logged on the RAID and decisions tab, not answered informally in a workshop.
- **Automate the capture where it repeats.** As one practitioner puts it, an as-built document is out of date as soon as you finish writing it. If an existing Intune tenant is in scope, export its configuration with tooling and keep the export in version control rather than transcribing it by hand.

## 3. Phases

**Phase 1 - Prepare (week 1).** Agree the scope of discovery, identify the owner for each domain, obtain read-only access to the consoles listed on the Tooling tab, and issue the workbook. Nothing here needs write access to any production system.

**Phase 2 - Automated capture (weeks 1-2).** Run the exports before the workshops, not after. Device inventory, Entra device and group exports, Conditional Access export, Group Policy XML export and analytics import, Configuration Manager application and task sequence reports, and the existing Intune tenant export if one exists. Workshops that start with data on the table are materially shorter.

**Phase 3 - Workshops and interviews (weeks 2-4).** Nine sessions, defined on the Workshops tab. Run W1 first because it sets scope. W7, the government and assurance session, needs the outputs of W2, W3 and W6, so schedule it late.

**Phase 4 - Audit periods (weeks 2-6, in parallel).** The elevation audit runs for two to four weeks, so start it in week 2 or it will delay the design. The same applies to any usage telemetry needed for application rationalisation.

**Phase 5 - Consolidate (week 5).** Close out the register, convert everything still open into RAID entries, and confirm the government feature-gap check. The design can start when every Must-priority row is answered or has an owned assumption.

## 4. Running the workshops

Each workshop on the Workshops tab names its attendees, duration, required inputs, outputs and the register rows it closes. Three points are worth stating outside the spreadsheet.

**Send the questions in advance.** The register is filterable by workshop. Send participants their filtered rows with the data exports already attached. A workshop is for resolving disagreement and capturing intent, not for reading out questions.

**Record intent, not just fact.** For every inherited control, ask why it exists and who would notice if it stopped. That answer is what makes the difference between a design that carries forward a policy baseline and one that carries forward a misunderstanding.

**Name an owner for every open item before the session ends.** An unowned question does not get answered between sessions.

## 5. Evidence checklist

By the end of discovery the following should exist as files, not statements:

- Device inventory export by platform, OS build, join state and agency, with Windows 11 hardware readiness.
- Entra export: devices, groups and their membership rules, role assignments, Conditional Access policies.
- Licence report showing SKUs held and counts.
- Group Policy XML export, plus the Group Policy analytics report showing supported, unsupported and deprecated settings.
- Application inventory with install counts, owners, packaging format and dependencies.
- Configuration Manager estate report: version, site systems, client health, collections, task sequences, distribution points.
- Network site list with bandwidth, proxy and TLS inspection position, and the endpoint allow-listing status.
- PKI documentation: issuing CAs, templates, connector hosts.
- Security baseline documentation and every approved deviation.
- Twelve months of endpoint ticket data.
- Classification policy, accreditation requirements and the privacy assessment position.
- If an Intune tenant already exists: a full configuration export.

## 6. Tooling and access

The Tooling tab lists fourteen data-collection routes with what each gathers, the permissions required and its caveats. Three points govern their use in a government context.

**Read-only is sufficient.** Every discovery activity in this pack can be performed with reader-level roles and read-only Graph scopes. Do not accept elevated access you do not need.

**Third-party tooling needs approval before it touches the tenant.** The community tools listed are widely used and genuinely useful, but they authenticate with an application registration against your tenant. In a government environment that is a change requiring assurance approval, and the code should be reviewed first. The Microsoft-published tenant documentation script is an alternative, with one important caveat: its repository was archived in September 2026 and is no longer maintained.

**Check which endpoint list applies.** Government tenants use different service endpoints from commercial tenants. Allow-listing the commercial endpoint list against a government tenant is a common and time-consuming mistake.

## 7. The government feature-gap check

This is the single highest-value activity in the pack, and the one most often skipped.

Microsoft maintains three tables in its Intune government service description: features supported in GCC High and DoD, features planned but not yet available, and features with no plan to support. Capabilities that most endpoint designs assume are present sit in the second and third tables. The Government tab lists twelve of them for explicit confirmation, including classic Windows Autopilot, Windows Autopatch and the Windows update policies, Remediations, the ServiceNow connector, BIOS and DFCI management, Device Health Attestation, and multi-session virtual desktops. Remote Help and Cloud PKI are available in GCC High but not DoD.

Two further points belong in the design rather than the gap list. GCC is not a separate Intune instance - for Intune, GCC means the commercial service, while GCC High and DoD are the physically separate government cloud, described by Microsoft as IL4 and IL5. And there is no built-in migration between the commercial service and the government cloud in either direction: every device must unenrol and re-enrol, which is a project phase, not a cutover task.

Confirm each item on the day the design is written. These tables move.

## 8. Source assessment

Fourteen sources are recorded on the Sources tab with publication dates, access dates and what each was used for. Three observations from assessing them:

**Comment sections yielded no corrections.** The instruction to check article comments for errors was followed on every community source that exposes them. Microsoft Learn carries no reader comments; feedback goes to GitHub. Of the community articles used, one carried a single comment, supportive, with no correction to the method; two had no comments; and one MVP article could not be read because the site returned a bot-verification challenge instead of the page. No source used here is contradicted by its own comment thread.

**The real risk was staleness, not error.** Two sources were demoted on inspection. Microsoft's own tenant documentation script repository was archived on 22 September 2026 and is unmaintained. The official IDPDIG table templates are version 1.0 from July 2024, so they predate both the 2026 government feature changes and the deployments feature now in preview - still a sound structure, but not a current statement of capability.

**One source is a trap.** Microsoft's "Migration checklists" page under the Configuration Manager documentation reads like Intune migration planning from its title. It covers Configuration Manager hierarchy-to-hierarchy migration and carries a 2016 date. It is recorded on the Sources tab as reviewed and deliberately not used, so that nobody re-finds it and assumes it was missed.

One authorship note: the Group Policy readiness method used to structure the GPO mapping tab comes from an author described as a Microsoft 365 architect and technical writer. MVP status could not be verified, so the article has been used for its method only, and every factual claim in this pack traces to Microsoft documentation instead.

## 9. What good looks like at the end

Discovery is complete when every Must-priority row is answered with evidence or has an owned, dated assumption; when the four decisions on the RAID tab have been taken or explicitly deferred with a named owner; when the government feature-gap check has been confirmed against Microsoft's current documentation; and when the jurisdiction is settled. That last point is worth repeating: until the jurisdiction is confirmed, section 15 of the HLD cannot be written accurately and the hosting decision cannot be closed.

At that point the design can start, and the HLD skeleton already produced becomes the structure it is written into.
