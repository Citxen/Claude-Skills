# Government and Public Sector Reference

Last reviewed: 2026-09-16. Items marked **Verify** must be confirmed during research; statuses change often.

Covers central, state and local government, defence, justice and public bodies.

## Regulations and standards

### United States

- **FISMA** and **NIST Risk Management Framework** (SP 800-37 Rev 2)
- **NIST SP 800-53 Rev 5**: Release 5.2.0 (August 2025) added software update, patch integrity and secure development controls. **Verify** later releases
- **FedRAMP**: Consolidated Rules for 2026 (CR26) launched June 2026; "FedRAMP Certified" replaces "FedRAMP Authorized". New 20x applications follow CR26 from July 2026; new Rev5 applications follow CR26 from 1 January 2027; no new Rev5 applications after 11 June 2027; Rev5 authorisations sunset by 31 December 2028. **Verify**
- **GovRAMP** (formerly StateRAMP) for state and local government cloud. **Verify** current requirements
- **CJIS Security Policy** for criminal justice information. **Verify** current version
- **IRS Publication 1075** for federal tax information
- **DoD Cloud Computing Security Requirements Guide** impact levels (IL2, IL4, IL5, IL6) and **CMMC** for defence contractors. **Verify** CMMC phase-in dates
- **OMB M-22-09** federal zero trust strategy and the **CISA Zero Trust Maturity Model v2**
- **CISA Trusted Internet Connections (TIC) 3.0**
- **NIST SP 800-218 (SSDF)** and the secure software development attestation form
- **FIPS 140-3** validated cryptography; **FIPS 203, 204 and 205** post-quantum algorithms (August 2024) and **NSM-10 / CNSA 2.0** migration timelines
- **Section 508** accessibility; the **DOJ ADA Title II rule** requires WCAG 2.1 AA for state and local government web content. **Verify** compliance dates
- **Federal Records Act** and NARA electronic records requirements
- **Privacy Act of 1974**, privacy impact assessments, and **CIRCIA** incident reporting. **Verify** CIRCIA final rule status

### United Kingdom

- **Government Cyber Security Strategy 2022–2030** and **GovAssure** (assurance based on the NCSC Cyber Assessment Framework)
- **NCSC Cyber Assessment Framework (CAF)**. **Verify** current version
- **Government Security Classifications Policy** (OFFICIAL, SECRET, TOP SECRET)
- **Cyber Essentials Plus** for suppliers
- **Secure by Design** for government digital services. **Verify** current mandate
- **GDS Service Standard**, **Technology Code of Practice**, **Cloud First** policy
- **Public Sector Bodies Accessibility Regulations**: WCAG 2.2 AA
- **UK GDPR, Data Protection Act 2018, Data (Use and Access) Act 2025**
- **Algorithmic Transparency Recording Standard** for algorithmic tools in the public sector
- **Cyber Security and Resilience Bill**: in the House of Lords as of July 2026. **Verify** Royal Assent and scope
- **Public Records Act** and National Archives digital preservation guidance

### European Union

- **NIS2**: public administration entities in scope. Transposition is uneven; the Commission referred Ireland, Spain, France and the Netherlands to the CJEU in July 2026. **Verify** the member state's transposition law
- **GDPR** and the **Law Enforcement Directive**
- **eIDAS 2.0** and the **European Digital Identity Wallet**. **Verify** member state wallet deadlines
- **Interoperable Europe Act**: interoperability assessments for cross-border public services
- **EU AI Act**: many public sector uses are high-risk (Annex III), some are prohibited. Annex III high-risk obligations are deferred to 2 December 2027 under the Digital Omnibus agreement. **Verify** formal adoption
- **Web Accessibility Directive** (EN 301 549)
- **EU Cybersecurity Certification Scheme for Cloud Services (EUCS)**. **Verify** adoption status
- **Data Act** and **Data Governance Act**

### Australia

- **Information Security Manual (ISM)**: updated quarterly. **Verify** current release
- **Essential Eight** maturity model
- **Protective Security Policy Framework (PSPF)**
- **IRAP** assessments and the **Hosting Certification Framework**
- **Digital Service Standard** (DTA)
- **Cyber Security Act 2024**: ransomware payment reporting within 72 hours

## Architecture concerns specific to the sector

- **Classification and sovereignty**: data classification drives hosting (sovereign cloud, government community cloud, on-premises for higher classifications), cleared personnel and supply chain nationality
- **Citizen identity**: reuse national identity services (e.g. Login.gov, GOV.UK One Login, myID, EUDI Wallet) instead of building new ones; identity proofing at NIST SP 800-63 IAL/AAL levels
- **Accessibility and assisted digital**: WCAG compliance and non-digital channels for digitally excluded users
- **Records management, FOI and transparency**: retention schedules, legal hold, disclosure-ready audit trails
- **Legacy modernisation**: mainframe and COBOL systems, strangler pattern, data migration with parallel running
- **Shared services and multi-tenancy** across departments or agencies with strict tenant isolation
- **Procurement constraints**: frameworks (e.g. G-Cloud, FedRAMP marketplace, BuyICT), open standards and open source preference, avoidance of lock-in
- **Long lifecycles and annual budget cycles**: design for 10+ year service life and incremental funding
- **Classified or air-gapped environments**: cross-domain solutions, offline update processes
- **Algorithmic accountability**: explainability, human review of automated decisions, equality impact assessment

## Indicative criticality baseline

Confirm against the organisation's business impact analysis.

| Service type | Availability | RTO | RPO |
|---|---|---|---|
| Emergency services, national security, benefits payments | 99.99% | under 1 hour | near zero |
| Citizen-facing transactional services | 99.9% to 99.95% | under 4 hours | under 1 hour |
| Case management and back office | 99.5% | 24 hours | 4 hours |
| Open data and information publishing | 99.5% | 48 hours | 24 hours |

## Common reference architectures to research

- AWS GovCloud and Secret Region, Azure Government, Google Distributed Cloud, Oracle Government Cloud, and national sovereign cloud offerings
- CISA Zero Trust Maturity Model and TIC 3.0 use cases
- UK NCSC Cloud Security Principles and GDS technology guidance
- Australian ISM cloud guidance and Hosting Certification Framework
