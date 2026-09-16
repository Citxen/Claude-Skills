# HLD Template Reference

Every HLD must contain each `##` section below, in this order, with the same titles. Replace every `{{...}}` block with real content. `scripts/validate_hld.py` reads the section titles and the rows of the ITIL practice and security control mapping tables from this file, so change the checks by changing this template.

Structure draws on ISO/IEC/IEEE 42010 (architecture description), TOGAF (principles, building blocks, ADM phases B to E), arc42, and the C4 model.

---

# High Level Design: {{Technology}} for {{Sector}}

## 1. Document Control

{{Table: document ID, version (start at 0.1 DRAFT), status, author, date, research date, classification (e.g. OFFICIAL / Internal / Confidential), review cycle. Then a table of approvers by role: Enterprise Architect, Security Architect, Service Owner, Data Protection Officer, Change Advisory Board. Then a change history table.}}

## 2. Executive Summary

{{Half a page for executives: the business problem, the proposed solution in two sentences, key decisions, headline risks, indicative cost range, and the decision being asked for.}}

## 3. Scope and Context

{{Business drivers and outcomes. In-scope and out-of-scope lists. Stakeholders and their concerns (42010 viewpoints). Current state summary and what changes.}}

## 4. Requirements

{{Tables with IDs. Business requirements (BR-nn). Functional requirements (FR-nn). Non-functional requirements (NFR-nn), grouped by availability, performance, scalability, security, privacy, compliance, operability, maintainability, portability, accessibility and sustainability. Every NFR has a measurable target and a column naming the component or control that meets it.}}

## 5. Architecture Principles

{{Table: each principle from architecture_principles.md, how this design applies it, and any deliberate exception with its justification and approver.}}

## 6. Solution Overview

{{C4 level 1 system context diagram in Mermaid, followed by a narrative. Then C4 level 2 container diagram in Mermaid. Name the architecture style and patterns used and why.}}

## 7. Logical Components

{{Table: component, responsibility, technology and version (researched), owner, build/buy/reuse decision, support and end-of-life date.}}

## 8. Integration Architecture

{{Interfaces table: ID, source, target, pattern (sync API, event, batch, file), protocol, data classification, authentication, volume and latency. API management, contract standards (e.g. OpenAPI, AsyncAPI, sector standards such as ISO 20022 or HL7 FHIR), versioning and error handling.}}

## 9. Data Architecture

{{Data entities and their classification, system of record, data flows (diagram), residency and sovereignty, retention and disposal, lineage, data quality, master data, backup, and privacy (lawful basis, minimisation, DPIA requirement).}}

## 10. Security Architecture

{{Zero trust approach (NIST SP 800-207). Identity and access (workforce, customer, machine, privileged). Network segmentation and trust zones (diagram). Encryption in transit and at rest, key management and HSM/FIPS 140-3 needs. Secrets management. Vulnerability and patch management. Logging for security (SIEM). Software supply chain (SBOM, signing). Threat model summary (STRIDE or sector method) with top threats and mitigating controls. Post-quantum cryptography readiness.}}

{{State the CIS Controls Implementation Group and justify it, and the CIS Benchmark (name, version, profile) for each major technology component. List any technology-specific frameworks applied from security_frameworks.md (e.g. CSA CCM, OWASP ASVS level, SLSA level). Then complete the control mapping table: one row per NIST CSF 2.0 function. Keep every row.}}

| CSF 2.0 Function | CIS Controls v8.1 | ISO/IEC 27001:2022 Annex A | Sector Framework | Design Controls | HLD Section |
|---|---|---|---|---|---|
| Govern | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |
| Identify | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |
| Protect | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |
| Detect | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |
| Respond | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |
| Recover | {{...}} | {{...}} | {{...}} | {{...}} | {{...}} |

## 11. Infrastructure and Deployment

{{Hosting model and justification. Environments (dev, test, pre-prod, prod, DR). Deployment view diagram in Mermaid. Regions and availability zones. Infrastructure as code, CI/CD pipeline and deployment strategy (blue/green, canary). Capacity baseline and scaling rules.}}

## 12. Resilience and Continuity

{{Service criticality tier. RTO, RPO and maximum tolerable downtime per service. HA design, failure modes and effects table, backup and immutable backup approach, DR strategy and test frequency, ransomware recovery, dependency and third-party concentration risk, exit strategy for critical suppliers, and important business service impact tolerances where regulation requires them.}}

## 13. Observability and Operations

{{Metrics, logs and traces (e.g. OpenTelemetry). SLIs and SLOs mapped to NFRs. Alerting and on-call. Runbooks. Operational support model (L1/L2/L3), hours of support, and automation of routine operations.}}

## 14. Service Management (ITIL) Alignment

{{State the ITIL version referenced. One paragraph on how the design supports the ITIL guiding principles and service value chain. Then complete the table: for each practice, the design response and the section of this HLD that delivers it. Keep every row.}}

| ITIL Practice | Design Response | HLD Section |
|---|---|---|
| Service level management | {{...}} | {{...}} |
| Availability management | {{...}} | {{...}} |
| Capacity and performance management | {{...}} | {{...}} |
| Service continuity management | {{...}} | {{...}} |
| Information security management | {{...}} | {{...}} |
| Change enablement | {{...}} | {{...}} |
| Release management | {{...}} | {{...}} |
| Deployment management | {{...}} | {{...}} |
| Monitoring and event management | {{...}} | {{...}} |
| Incident management | {{...}} | {{...}} |
| Problem management | {{...}} | {{...}} |
| Service configuration management | {{...}} | {{...}} |
| IT asset management | {{...}} | {{...}} |
| Supplier management | {{...}} | {{...}} |
| Knowledge management | {{...}} | {{...}} |
| Service catalogue management | {{...}} | {{...}} |

## 15. Regulatory Compliance Mapping

{{Table: regulation or standard, jurisdiction, status as researched (in force / proposed / transition), requirement, design control, HLD section, evidence the control will produce. Mark anything unconfirmed as "To confirm".}}

## 16. Architecture Decisions

{{At least three ADRs. Each: ID, title, status, context, options considered (at least two), decision, consequences, and principles or requirements it serves.}}

## 17. Risks, Assumptions, Issues and Dependencies

{{RAID tables. Risks have likelihood, impact, owner and mitigation. Include open issues that need a human decision, especially unconfirmed regulatory points.}}

## 18. Cost and Sustainability

{{Cost drivers, licensing model, indicative run and build cost ranges with the assumptions behind them, FinOps controls, and sustainability considerations (carbon-aware region choice, right-sizing, retention).}}

## 19. Transition and Roadmap

{{Phases, migration approach, transition to live service (early life support, service acceptance criteria, operational readiness), decommissioning, and architecture governance checkpoints.}}

## 20. Glossary

{{Terms and acronyms used in this document.}}

## 21. References

{{Every source used, as a markdown link with its access date, grouped into standards and regulations, vendor documentation, and industry guidance.}}
