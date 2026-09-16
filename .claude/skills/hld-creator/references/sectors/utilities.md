# Utilities Sector Reference

Last reviewed: 2026-09-16. Items marked **Verify** must be confirmed during research; statuses change often.

Covers electricity generation, transmission and distribution, gas, water and wastewater.

## Regulations and standards

### Cross-jurisdiction

- **ISA/IEC 62443** series: industrial automation and control system security (zones and conduits, security levels, supplier requirements)
- **IEC 62351**: security for power system communication protocols
- **IEC 61850** (substation automation) and **IEC 61968/61970** (Common Information Model)
- **NIST SP 800-82 Rev 3**: OT security guide
- **NIST CSF 2.0** and **ISO/IEC 27001:2022** plus **ISO/IEC 27019** (energy utility controls)

### United States

- **NERC CIP Reliability Standards** (CIP-002 to CIP-015) for the bulk electric system:
  - **CIP-015-1** internal network security monitoring: effective 2 September 2025; high and medium impact BES Cyber Systems with external routable connectivity must implement it by 1 October 2028, others by 1 October 2030. CIP-015-2 is in development. **Verify**
  - **CIP-013** supply chain risk management; **CIP-003** low impact controls. **Verify** current versions and effective dates
  - Virtualisation and cloud-related revisions. **Verify** status
- **DOE Cybersecurity Capability Maturity Model (C2M2) v2.1**
- **TSA Security Directives** for pipelines. **Verify** current directive revision
- **America's Water Infrastructure Act (AWIA) 2018**: risk and resilience assessments and emergency response plans for community water systems; EPA cybersecurity guidance
- **CIRCIA** incident reporting. **Verify** final rule status
- **State public utility commission** rules on smart meter data privacy and cost recovery

### European Union

- **NIS2**: energy, drinking water and wastewater are sectors of high criticality. **Verify** the member state's transposition law
- **Critical Entities Resilience (CER) Directive**: member states identify critical entities, which must then carry out resilience risk assessments. **Verify** national timelines
- **Network Code on Cybersecurity for electricity** (Delegated Regulation (EU) 2024/1366): cross-border electricity flows risk assessment cycle
- **REMIT** for wholesale energy market integrity
- **Cyber Resilience Act**: manufacturer vulnerability reporting obligations apply from 11 September 2026; full requirements from 11 December 2027. Relevant to OT product procurement
- **GDPR** for smart meter data

### United Kingdom

- **NIS Regulations 2018**: operators of essential services in energy and water, assessed against the NCSC CAF by Ofgem, DESNZ, DWI and Defra
- **Cyber Security and Resilience Bill**: in the House of Lords as of July 2026, expands NIS scope and incident reporting. **Verify** Royal Assent
- **Security and Emergency Measures Direction (SEMD)** for water
- **Ofgem** licence conditions and RIIO price control requirements for data and digitalisation (e.g. Data Best Practice guidance)

### Australia

- **Security of Critical Infrastructure (SOCI) Act 2018**: critical infrastructure risk management programme (CIRMP) and mandatory incident reporting
- **Australian Energy Sector Cyber Security Framework (AESCSF)**

## Architecture concerns specific to the sector

- **IT/OT segmentation**: Purdue model and ISA-95 levels, IEC 62443 zones and conduits, an industrial DMZ between enterprise and control networks, unidirectional gateways for high-impact sites
- **Safety first**: safety instrumented systems isolated from control and enterprise networks; changes assessed for process safety impact
- **Deterministic and real-time behaviour**: SCADA, EMS, ADMS and protection systems with strict latency and jitter budgets
- **Legacy and insecure protocols**: Modbus, DNP3, IEC 60870-5-104; use DNP3 Secure Authentication or IEC 62351 where possible, and compensating monitoring where not
- **Long asset lifecycles** (20 to 40 years) and restricted patch windows; virtual patching and compensating controls
- **Remote and constrained sites**: substations, pumping stations and pipelines with limited bandwidth, private LTE/5G, satellite backup
- **Scale of edge devices**: smart meters (AMI), DER, IoT sensors; device identity, certificate lifecycle, OTA update security
- **Operational data**: time-series historians, GIS, outage management (OMS), DERMS, asset performance management
- **Cloud for OT**: regulators allow limited cloud use for OT; keep real-time control on premises and justify any cloud dependency. **Verify** current NERC guidance
- **Vendor remote access**: brokered, recorded, time-bound sessions with MFA
- **Physical and climate resilience**: flood, heat and wildfire risk to sites; black start and islanding capability; manual fallback operations
- **Internal network security monitoring** of east-west OT traffic (CIP-015)

## Indicative criticality baseline

Confirm against the organisation's business impact analysis and safety case.

| Service type | Availability | RTO | RPO |
|---|---|---|---|
| SCADA, EMS, protection and control | 99.999% with manual fallback | seconds to minutes (hot standby) | zero for control state |
| Outage management, ADMS, DERMS | 99.99% | under 1 hour | under 5 minutes |
| Meter data management, billing | 99.9% | 8 hours | 1 hour |
| Enterprise asset management, analytics | 99.5% | 24 hours | 4 hours |

## Common reference architectures to research

- ISA/IEC 62443 reference zone models and the Purdue Enterprise Reference Architecture
- EPRI and NIST smart grid reference architectures (NIST Framework for Smart Grid Interoperability)
- NERC guidance on cloud and virtualisation for BES Cyber Systems
- Vendor OT reference designs (e.g. Siemens, Schneider Electric, ABB, GE Vernova, Hitachi Energy)
- AWS, Azure and Google Cloud energy and utilities industry architectures for non-real-time workloads
