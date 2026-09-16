# ITIL Alignment Reference

Last reviewed: 2026-09-16

## Version status

- **ITIL (Version 5)** was launched by PeopleCert in early 2026 (Foundation released February 2026, further modules through 2026). It unifies digital product and service management, adds a product-centric lifecycle and AI governance guidance
- **ITIL 4** remains widely used and runs alongside Version 5 during the transition
- **Verify** during research: which version the HLD should reference, and whether Version 5 renamed any practice listed below. If a name changed, keep the row name from the template and add the new name in brackets in the Design Response

## Guiding principles

Show how the design reflects each one in section 14:

1. Focus on value: requirements trace to service outcomes for customers, citizens or patients
2. Start where you are: reuse existing platforms, tooling and CMDB data
3. Progress iteratively with feedback: phased roadmap with measurable checkpoints
4. Collaborate and promote visibility: named owners, shared dashboards, documented decisions
5. Think and work holistically: cover the four dimensions below, not just technology
6. Keep it simple and practical: avoid controls and processes that add no value
7. Optimise and automate: automate change, deployment, monitoring and recovery where safe

## Four dimensions of service management

The HLD must address each:

- **Organisations and people**: support model, skills, roles and responsibilities (RACI)
- **Information and technology**: the architecture itself, data and knowledge
- **Partners and suppliers**: suppliers, contracts, SLAs/OLAs, concentration and exit
- **Value streams and processes**: how demand becomes value, and the processes that operate the service

## Service value chain

Map design activities to: plan, improve, engage, design and transition, obtain/build, deliver and support.

## What each practice needs from an HLD

| Practice | Design must provide |
|---|---|
| Service level management | SLIs, SLOs and the SLA targets they support; how they are measured |
| Availability management | Availability target, HA design, planned maintenance approach |
| Capacity and performance management | Capacity baseline, growth forecast, scaling rules, performance targets |
| Service continuity management | Criticality tier, RTO/RPO, DR strategy and test schedule |
| Information security management | Controls, risk assessment, alignment to ISO/IEC 27001:2022 or sector framework |
| Change enablement | Change types (standard, normal, emergency), what can be pre-approved standard change via automation |
| Release management | Release cadence, versioning, feature flags |
| Deployment management | Pipeline, deployment strategy, rollback |
| Monitoring and event management | Telemetry, event correlation, alert routing to incident tooling |
| Incident management | Incident categories, priority model, integration with ITSM tool, regulatory incident reporting timelines |
| Problem management | Root cause analysis inputs (logs, traces), known error records |
| Service configuration management | Configuration items to register in the CMDB and how discovery keeps them current |
| IT asset management | Licences, hardware and cloud assets, lifecycle and end-of-life tracking |
| Supplier management | Critical suppliers, contractual controls, performance monitoring, exit plans |
| Knowledge management | Runbooks, architecture records, known errors, where they live |
| Service catalogue management | Catalogue entry, request offerings, service owner |

## Related standards

- ISO/IEC 20000-1:2018 (service management system)
- COBIT 2019 (governance of enterprise IT)
- VeriSM and SIAM where multiple suppliers deliver the service
