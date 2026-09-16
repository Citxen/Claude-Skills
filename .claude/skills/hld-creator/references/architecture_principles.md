# Architecture Principles Reference

Apply every principle below. Section 5 of the HLD must show how the design meets each one, or record a justified exception. Principles follow the TOGAF format (statement, rationale, implications) and draw on the AWS, Azure and Google Cloud Well-Architected Frameworks, NIST SP 800-207 (zero trust), and ISO/IEC/IEEE 42010.

## Business principles

1. **Business value first**
   - Statement: every component traces to a business requirement or outcome
   - Implications: remove components with no requirement; measure outcomes, not outputs
2. **Compliance by design**
   - Statement: regulatory and policy obligations are designed in, not audited in
   - Implications: every obligation in section 15 maps to a control and the evidence it produces
3. **Service continuity for important business services**
   - Statement: design to stay within impact tolerances for the services customers, citizens or patients depend on
   - Implications: set criticality before choosing technology; test severe but plausible scenarios

## Data principles

4. **Data is an asset with an owner**
   - Implications: each data entity has an owner, a classification and a system of record
5. **Privacy by design and by default** (GDPR Article 25, ISO/IEC 27701)
   - Implications: minimise collection, pseudonymise where possible, define retention and disposal
6. **Data sovereignty and residency are explicit**
   - Implications: state where data is stored, processed and supported from, including backups and logs

## Application principles

7. **Reuse before buy before build**
   - Implications: justify any new build against existing enterprise platforms and SaaS
8. **Loose coupling through well-defined interfaces**
   - Implications: versioned API and event contracts; no shared databases between services
9. **Open standards and portability**
   - Implications: prefer open protocols and formats; state lock-in and an exit strategy for each critical supplier

## Technology principles

10. **Zero trust security** (NIST SP 800-207)
    - Implications: never trust network location; authenticate and authorise every request; least privilege; assume breach
11. **Defence in depth and secure by default**
    - Implications: layered controls; secure configuration baselines (e.g. CIS Benchmarks); deny by default
12. **Design for failure**
    - Implications: no single points of failure for critical services; graceful degradation; automated recovery
13. **Observable by default**
    - Implications: every component emits metrics, logs and traces tied to SLOs
14. **Automate everything repeatable**
    - Implications: infrastructure and policy as code; automated testing and deployment; no manual production changes
15. **Supported technology only**
    - Implications: no component past end of support during the planned life of the service; track end-of-life dates
16. **Cost-aware and sustainable**
    - Implications: right-size, scale to demand, tag for cost allocation, consider carbon intensity of regions
17. **Keep it simple**
    - Implications: choose the simplest design that meets the requirements; justify added complexity in an ADR

## Well-Architected pillars

Check the design against all six pillars shared by the major cloud frameworks, even for on-premises designs:

- Operational excellence
- Security
- Reliability
- Performance efficiency
- Cost optimisation
- Sustainability
