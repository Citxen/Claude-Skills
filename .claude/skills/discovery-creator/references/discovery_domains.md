# Discovery Domains Reference

Every discovery pack covers these seventeen domains. They are sector-neutral: the matched sector
file in `.claude/skills/hld-creator/references/sectors/` supplies the regulatory content for
domain L, and shapes the classification, residency and assurance questions elsewhere.

A pack may add a domain the technology demands. It may not drop one; if a domain does not apply,
keep it and say why in a single row, so the reader can see the decision was taken.

The "feeds" column names the section of `.claude/skills/hld-creator/references/hld_template.md`
that consumes the answers. Every question in the register carries one, and a question that feeds
no section should not be asked.

| Ref | Domain | What it establishes | Feeds |
|---|---|---|---|
| A | Objectives and scope | Outcomes wanted, what is in and out, immovable dates, who approves, appetite for disruption | 2, 3, 4, 19 |
| B | Organisation | Team, skills, clearances, outsourcing, support model, change process, CMDB, current admin roles | 13, 14 |
| C | Estate | What exists: counts, versions, ownership, join or management state, age, locations, the unmanaged remainder | 3, 7, 11, 19 |
| D | Personas | Who uses it and how: applications, data handled, connectivity, privilege, accessibility | 3, 4, 7 |
| E | Licensing and cost | Entitlements held against entitlements required, incumbent contracts and exit, budget and chargeback | 18 |
| F | Identity and access | Tenants, directory topology, authentication, groups, delegated administration, conditional access | 8, 10 |
| G | Existing policy | Inherited configuration and its intent: policies, baselines, scripts, imaging, incumbent tooling | 7, 10, 19 |
| H | Applications | Inventory, ownership, packaging, dependencies, rationalisation, who patches what | 7, 18 |
| I | Updates | Current patching process, cadence, mandated timelines, maintenance windows, content delivery | 11, 12 |
| J | Security | Protection in place, privilege, encryption, logging, vulnerability management, target baseline and maturity | 10 |
| K | Network and connectivity | Sites, bandwidth, proxy and inspection, endpoint reachability, certificates, retained on-premises dependencies | 8, 11 |
| L | Sector and regulatory | Jurisdiction, environment, classification, accreditation route, sector obligations, supplier assurance | 9, 15 |
| M | Data and privacy | Personal data, lawful basis, impact assessment, retention, records, legal hold, telemetry constraints | 9 |
| N | Service management | Ticket baseline, recurring failures, remote support, self-service, reporting expectations | 13, 14 |
| O | Resilience | Criticality, RTO and RPO, recovery at scale, configuration backup, exit and portability | 12, 16 |
| P | Rollout | Rings and pilots, communications, training, freeze periods, success measures, rollback | 19 |
| Q | Migration source | The specific estate being moved from, its dependencies and its decommissioning | 19 |

## Question quality

Each row of the register must carry all of:

- **A question that has a single answer.** Split anything compound. "Counts and versions and owners"
  is three rows, and three different people answer them.
- **How to obtain it**: a named report, export, console, script or interview. Not "investigate".
  Prefer an export over an opinion wherever an export exists.
- **Who owns the answer**: a role, never a person's name.
- **A priority**: Must, Should or Could. Must means the design cannot be written without it.
- **A workshop reference** that exists on the Workshops sheet.
- **The HLD section it feeds.**

## Audit periods

Some answers cannot be gathered in a workshop because they need observation over time. Identify
these in the pack and start them in week one, or they become the critical path:

- Privilege: what users actually elevate, observed in a reporting-only mode before rights change
- Application usage: what is genuinely used, over a period long enough to cover monthly cycles
- Device activity: telemetry-based readiness reporting only counts devices that checked in recently

## Feature gaps

Where the technology behaves differently in the deployment the sector demands - a government cloud,
a sovereign region, an air-gapped build - the pack carries a flag column on the register and a
dedicated sheet listing each capability for explicit confirmation. Record the availability, the
source checked and the date checked, because these move faster than any other fact in the pack.
