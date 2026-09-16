# Financial Services Sector Reference

Last reviewed: 2026-09-16. Items marked **Verify** must be confirmed during research; statuses change often.

Covers banking, payments, insurance, capital markets and fintech.

## Regulations and standards

### Cross-jurisdiction

- **PCI DSS v4.0.1**: the only active version; all future-dated requirements mandatory since 31 March 2025. Applies wherever cardholder data is stored, processed or transmitted. Also PCI PIN and PCI HSM for payment cryptography. **Verify** no newer version
- **SWIFT Customer Security Controls Framework (CSCF)**: updated annually, with yearly attestation. **Verify** the current version
- **ISO 20022** messaging for payments; cross-border coexistence with MT messages ended November 2025
- **BCBS 239** (risk data aggregation) and **BCBS Principles for Operational Resilience**
- **ISO/IEC 27001:2022**, **SOC 2**, **NIST CSF 2.0**, **CIS Controls v8.1**
- **EU AI Act**: creditworthiness and life/health insurance pricing AI are high-risk (Annex III). The Digital Omnibus provisional agreement (May 2026) defers Annex III high-risk obligations to 2 December 2027. **Verify** formal adoption

### European Union

- **DORA** (Regulation (EU) 2022/2554): applies since 17 January 2025. ICT risk management framework, major ICT incident reporting, digital operational resilience testing, TLPT every three years for designated entities (RTS (EU) 2025/1190, TIBER-EU aligned), register of information for ICT third-party arrangements, concentration risk and exit strategies. Critical ICT third-party providers (CTPPs) are designated and overseen by the ESAs
- **NIS2**: financial entities are in scope, but DORA applies as sector-specific law for ICT risk
- **GDPR**
- **PSD2** strong customer authentication; **PSD3 and the Payment Services Regulation**. **Verify** adoption and application dates
- **Instant Payments Regulation**: verification of payee and instant euro credit transfers. **Verify** which deadlines apply to the institution
- **MiCA** for crypto-asset service providers
- **EBA Guidelines on outsourcing** and ICT and security risk management

### United Kingdom

- **PRA SS1/21 and FCA PS21/3 operational resilience**: important business services, impact tolerances, mapping and scenario testing; full compliance required since 31 March 2025
- **PRA SS2/21** outsourcing and third-party risk management
- **Critical third parties regime** (PRA PS16/24, FCA PS24/16): in force since 1 January 2025; HM Treasury designates CTPs. **Verify** designations
- **CBEST** intelligence-led testing
- **UK GDPR, Data Protection Act 2018, Data (Use and Access) Act 2025**
- **FCA Consumer Duty**
- **Cyber Security and Resilience Bill**: in the House of Lords as of July 2026. **Verify** Royal Assent and scope

### United States

- **Gramm-Leach-Bliley Act Safeguards Rule** (FTC) and banking agency equivalents
- **Sarbanes-Oxley** IT general controls for financial reporting systems
- **FFIEC IT Examination Handbook**. The FFIEC Cybersecurity Assessment Tool was sunset in August 2025; examiners point to NIST CSF 2.0 and CISA CPGs
- **NYDFS 23 NYCRR Part 500**: amended requirements fully phased in by November 2025 (MFA, asset inventory, CISO reporting, 72-hour notification)
- **SEC cybersecurity disclosure rules**: material incidents on Form 8-K Item 1.05 within four business days
- **SEC Regulation S-P amendments**: incident response programme and customer notification within 30 days. **Verify** compliance dates for the entity's size
- **SEC Rule 17a-4**: electronic records retention (WORM or audit-trail alternative)
- **Interagency Guidance on Third-Party Relationships** (June 2023)
- **SR 11-7** model risk management, applied to AI and ML models

### Asia-Pacific

- **Australia APRA CPS 230** operational risk management: in force since 1 July 2025. **CPS 234** information security
- **Singapore MAS Technology Risk Management Guidelines** and MAS Notices on cyber hygiene
- **Hong Kong HKMA** Operational Resilience (SPM OR-2) and Cyber Resilience Assessment Framework. **Verify** current versions

## Architecture concerns specific to the sector

- **Consistency and integrity**: double-entry ledgers, idempotent transaction processing, exactly-once semantics, reconciliation
- **Audit and non-repudiation**: immutable, time-synchronised audit trails; digital signatures; records retention by regulation (commonly 5 to 7 years, longer for some records)
- **Segregation of duties and four-eyes controls** for privileged and payment operations
- **Payment cryptography**: HSMs (FIPS 140-3 Level 3, PCI HSM), tokenisation, point-to-point encryption, key ceremonies
- **Cardholder data environment scope reduction**: tokenisation and network segmentation to shrink PCI scope
- **Fraud and financial crime**: real-time fraud scoring, AML transaction monitoring, sanctions screening in the payment path with latency budgets
- **Cloud concentration risk and exit strategy**: DORA and PRA require documented, tested exit plans for critical ICT providers
- **Low latency** for trading and payments; time synchronisation (MiFID II RTS 25 clock accuracy for trading)
- **Model risk** for AI: explainability, bias testing, human oversight, model inventory
- **Open banking APIs**: FAPI 2.0 security profile, consent management

## Indicative criticality baseline

Confirm against the organisation's business impact analysis and stated impact tolerances.

| Service type | Availability | RTO | RPO |
|---|---|---|---|
| Payments, card authorisation, core ledger | 99.99% or higher | under 2 hours (within impact tolerance) | near zero |
| Customer channels (mobile, online banking) | 99.95% | under 4 hours | under 15 minutes |
| Trading and market access | 99.99% in market hours | minutes | near zero |
| Internal reporting and analytics | 99.5% | 24 hours | 4 hours |

## Common reference architectures to research

- AWS Financial Services industry lens, Azure Financial Services cloud and landing zones, Google Cloud financial services blueprints
- BIAN (Banking Industry Architecture Network) service landscape
- FINOS open-source standards (e.g. Common Domain Model, CCC cloud controls)
- EBA and ECB guidance on cloud outsourcing
