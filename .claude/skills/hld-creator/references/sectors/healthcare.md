# Healthcare Sector Reference

Last reviewed: 2026-09-16. Items marked **Verify** must be confirmed during research; statuses change often.

Covers providers, payers, public health, life sciences, and health technology suppliers.

## Regulations and standards

### Cross-jurisdiction

- **HL7 FHIR** (R4 is the version most regulations mandate; R5 published), **SMART on FHIR**, **CDS Hooks**. **Verify** R6 status
- **DICOM** and **DICOMweb** for imaging; **IHE** integration profiles
- **SNOMED CT**, **LOINC**, **ICD-10** and **ICD-11** terminologies
- **ISO 27799** (health information security), **IEC 80001-1:2021** (medical IT networks), **IEC 62304** (medical device software lifecycle), **ISO 14971** (risk management), **ISO 13485**
- **HITRUST CSF**. **Verify** current version

### United States

- **HIPAA Privacy, Security and Breach Notification Rules** and **HITECH**
- **HIPAA Security Rule update**: proposed rule published 6 January 2025 (mandatory encryption, MFA, asset inventory, annual penetration testing, 72-hour restoration planning). Still not final as of September 2026; the regulatory agenda shows final action due July 2027. Design to the proposed controls as good practice, but cite the current rule as the legal requirement. **Verify**
- **HHS 405(d) Health Industry Cybersecurity Practices** (recognised security practices) and **HHS Healthcare Cybersecurity Performance Goals**
- **21st Century Cures Act information blocking** rules
- **ONC Health IT Certification Program**: HTI-1 in force; **HTI-5 proposed rule** (January 2026) would remove or revise most certification criteria and prioritise FHIR APIs; comment period closed 27 February 2026, not yet final. **Verify**
- **CMS Interoperability and Prior Authorization Final Rule (CMS-0057-F)**: payer FHIR APIs, most due from 1 January 2027. **Verify**
- **TEFCA** (Qualified Health Information Networks) and **USCDI** data classes. **Verify** current USCDI version required
- **42 CFR Part 2** for substance use disorder records: aligned with HIPAA, compliance required from 16 February 2026
- **FDA Section 524B** cyber device requirements (SBOM, vulnerability management) and FDA premarket cybersecurity guidance. **Verify** latest guidance
- **FTC Health Breach Notification Rule** for health apps not covered by HIPAA
- **State laws**: e.g. Washington My Health My Data Act, California CMIA

### European Union

- **GDPR**: health data is special category data (Article 9); DPIA usually required
- **European Health Data Space (EHDS) Regulation**: in force 26 March 2025; general application 26 March 2027, with further milestones in 2029, 2031 and 2035 for EHR system requirements, primary use exchange formats and secondary use. **Verify** which milestone applies to the design
- **NIS2**: healthcare providers are in scope. **Verify** the member state's transposition law
- **Medical Device Regulation (EU) 2017/745** and **IVDR (EU) 2017/746** for software as a medical device
- **EU AI Act**: medical AI regulated as a product under Annex I; high-risk obligations deferred to 2 August 2028 under the Digital Omnibus agreement. **Verify** formal adoption
- **Cyber Resilience Act**: vulnerability reporting from 11 September 2026 for products with digital elements not covered by MDR

### United Kingdom

- **UK GDPR, Data Protection Act 2018, Data (Use and Access) Act 2025**; **Caldicott Principles**; common law duty of confidentiality; National Data Opt-out
- **NHS Data Security and Protection Toolkit (DSPT)**: CAF-aligned for NHS trusts and other large bodies; new directive cyber policies (MFA, high-severity alerts, endpoint detection) included from September 2026. **Verify**
- **DCB0129 and DCB0160** clinical risk management standards: clinical safety case and hazard log. **Verify** current revisions
- **NHS Digital Technology Assessment Criteria (DTAC)**
- **MHRA** software and AI as a medical device regulation. **Verify** post-Brexit device regulation changes
- **NHS standards**: NHS Login, NHS number, FHIR UK Core, Spine, NHS Care Identity Service 2, NHS cloud security guidance
- **Cyber Security and Resilience Bill**: in the House of Lords as of July 2026, brings more healthcare suppliers and managed service providers into scope. **Verify**

### Australia

- **Privacy Act 1988** (2024 amendments) and **My Health Records Act 2012**
- **Australian Digital Health Agency** standards and the national FHIR profiles (AU Core)
- **SOCI Act** for critical hospitals

## Architecture concerns specific to the sector

- **Patient safety**: clinical safety case and hazard log for any system that affects care; clinical safety officer sign-off; design out hazards such as wrong-patient records and stale data
- **Availability and downtime procedures**: 24x7 clinical operation; read-only downtime viewers and paper fallback when systems fail; well-rehearsed business continuity
- **Ransomware resilience**: sector is heavily targeted (e.g. Change Healthcare and Synnovis incidents in 2024); immutable offline backups, segmented recovery environment, tested restoration time
- **Access control**: role- and context-based access, break-glass emergency access with retrospective review, audit of every record access
- **Consent and preferences**: consent management, opt-outs, sensitive record segmentation (e.g. 42 CFR Part 2, sexual health, mental health)
- **Identity matching**: enterprise master patient index, probabilistic matching and duplicate resolution
- **Interoperability**: FHIR APIs first, HL7 v2 integration engines for legacy, terminology services
- **Medical device networks**: segment and monitor devices that cannot be patched (IEC 80001-1), device inventory and SBOMs
- **Secondary use**: de-identification (HIPAA Safe Harbor or Expert Determination), pseudonymisation, trusted research environments and secure data environments
- **Clinical AI**: regulatory classification, validation on local populations, human oversight, bias monitoring, post-market surveillance
- **Data residency**: many jurisdictions restrict offshoring of patient data and support access

## Indicative criticality baseline

Confirm against the organisation's business impact analysis and clinical safety assessment.

| Service type | Availability | RTO | RPO |
|---|---|---|---|
| EHR, medication administration, emergency department, theatres | 99.99% with downtime procedures | under 1 hour | under 5 minutes |
| Imaging (PACS), laboratory systems | 99.95% | under 2 hours | under 15 minutes |
| Patient portal, appointment booking | 99.9% | 8 hours | 1 hour |
| Research and analytics platforms | 99.5% | 48 hours | 24 hours |

## Common reference architectures to research

- AWS for Health, Microsoft Cloud for Healthcare and Azure Health Data Services, Google Cloud Healthcare API
- HL7 FHIR implementation guides for the jurisdiction (US Core, UK Core, AU Core, EHDS profiles)
- NHS England secure data environment and federated data platform guidance
- HHS 405(d) resources and CISA healthcare sector guidance
