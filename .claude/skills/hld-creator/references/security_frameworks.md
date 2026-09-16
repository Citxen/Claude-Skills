# Security Frameworks Reference

Last reviewed: 2026-09-16. Items marked **Verify** must be confirmed during research.

Section 10 of the HLD must map the design's security controls to these frameworks using the control mapping table in `hld_template.md`. NIST CSF 2.0 is the organising spine because most other frameworks publish mappings to it.

## Baseline frameworks (apply to every HLD)

- **NIST Cybersecurity Framework (CSF) 2.0** (February 2024): six functions (Govern, Identify, Protect, Detect, Respond, Recover). One mapping table row per function
- **CIS Critical Security Controls v8.1** (June 2024): 18 Controls, 153 Safeguards, three Implementation Groups. v8.1 added the Govern function to align with CSF 2.0. **Verify** no newer version
- **CIS Benchmarks**: secure configuration baselines for the specific technology (operating systems, databases, Kubernetes, cloud accounts, network devices). State the Benchmark name, version and profile (Level 1, Level 2, or STIG profile), and whether CIS Hardened Images are used
- **ISO/IEC 27001:2022 and ISO/IEC 27002:2022**: 93 Annex A controls in four themes (organisational 5.x, people 6.x, physical 7.x, technological 8.x). Amendment 1:2024 added climate change considerations to clause 4
- **NIST SP 800-207** zero trust architecture and the **CISA Zero Trust Maturity Model v2**

## Choosing the CIS Implementation Group

State the Implementation Group in section 10 and justify it:

- **IG1**: basic cyber hygiene. Not sufficient on its own for regulated sectors
- **IG2**: enterprises with regulatory obligations and multiple departments. The minimum for any HLD in these four sectors
- **IG3**: services handling sensitive data or critical functions, where attacks would cause significant harm to the public. The default for payments, national security, OT control systems, and clinical systems

## Indicative mapping to the CSF 2.0 functions

Use this as a starting point; confirm against the official CIS Controls v8.1 to CSF 2.0 mapping and the NIST CSF 2.0 informative references.

| CSF 2.0 Function | CIS Controls v8.1 | ISO/IEC 27001:2022 Annex A |
|---|---|---|
| Govern | Process and policy Safeguards across Controls (e.g. 3.1, 4.1, 7.1, 15.1, 15.2, 17.1, 18.1); 14 Security Awareness; 15 Service Provider Management | 5.1–5.4 policies and roles; 5.19–5.23 supplier and cloud services; 5.31–5.36 compliance |
| Identify | 1 Enterprise Asset Inventory; 2 Software Asset Inventory; 3 Data Protection (classification and inventory); 7 Continuous Vulnerability Management | 5.9 inventory; 5.12 classification; 8.8 technical vulnerabilities |
| Protect | 3 Data Protection; 4 Secure Configuration; 5 Account Management; 6 Access Control Management; 9 Email and Browser Protections; 10 Malware Defences; 12 Network Infrastructure Management; 16 Application Software Security | 5.15–5.18 access control and identity; 8.2–8.5 privileged access and authentication; 8.9 configuration; 8.20–8.22 network security; 8.24 cryptography; 8.25–8.29 secure development |
| Detect | 8 Audit Log Management; 13 Network Monitoring and Defence; 10 Malware Defences (detection) | 8.15 logging; 8.16 monitoring activities |
| Respond | 17 Incident Response Management | 5.24–5.28 incident management and evidence |
| Recover | 11 Data Recovery; 17 post-incident review | 5.29–5.30 continuity and ICT readiness; 8.13 backup; 8.14 redundancy |

## Sector frameworks for the mapping table's sector column

- **Financial**: PCI DSS v4.0.1, DORA ICT risk management RTS, NYDFS Part 500, FFIEC, CRI Profile (built on CSF 2.0; **Verify** current version), SWIFT CSCF, APRA CPS 234, MAS TRM
- **Government**: NIST SP 800-53 Rev 5 control baselines and FedRAMP baselines, DISA STIGs, NCSC CAF, Australian ISM and Essential Eight
- **Utilities**: ISA/IEC 62443 (security levels, zones and conduits), NERC CIP, DOE C2M2 v2.1, NCSC CAF, AESCSF
- **Healthcare**: HHS 405(d) HICP, HPH Cybersecurity Performance Goals, HITRUST CSF, NHS DSPT (CAF-aligned), ISO 27799

## Technology-specific frameworks (apply when relevant)

- **Cloud**: CSA Cloud Controls Matrix (CCM) v4.1 (January 2026; STAR assessments must use it from July 2027) and CAIQ v4.1; the cloud provider's Well-Architected security pillar and CIS Foundations Benchmark
- **Containers and Kubernetes**: NIST SP 800-190, CIS Kubernetes and Docker Benchmarks, NSA/CISA Kubernetes Hardening Guidance
- **Applications and APIs**: OWASP ASVS 5.0.0 (state the verification level: L1, L2 or L3; L2 minimum for regulated data), OWASP Top 10 and OWASP API Security Top 10. **Verify** current Top 10 editions
- **Software supply chain**: NIST SP 800-218 (SSDF), SLSA v1.2 (state the build level), SBOMs in SPDX or CycloneDX, signed artefacts (e.g. Sigstore)
- **AI and ML**: NIST AI RMF 1.0 and its generative AI profile, ISO/IEC 42001:2023, OWASP Top 10 for LLM Applications, MITRE ATLAS
- **Operational technology**: ISA/IEC 62443, NIST SP 800-82 Rev 3, MITRE ATT&CK for ICS
- **Cryptography**: FIPS 140-3 validated modules; post-quantum migration to FIPS 203, 204 and 205 following NIST IR 8547 transition timelines. **Verify** the IR 8547 status
- **Identity**: NIST SP 800-63 digital identity guidelines (assurance levels IAL, AAL, FAL). **Verify** whether Revision 4 is final

## Threat modelling

- Use **STRIDE** for design-level threats and **MITRE ATT&CK** (Enterprise, Cloud, ICS or Mobile matrix as relevant) to map the top threats to detections and mitigations
- Use **MITRE D3FEND** to name the defensive techniques
- Record the top threats in section 10 with the CIS Safeguards or other controls that mitigate each one
