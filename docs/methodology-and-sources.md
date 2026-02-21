# Data Sources and Methodology (February 2026)

This document describes the data sources and methodology underlying the Impact-First Security Model (IFSM) and Impact Forecast Algorithm (IFA). All claims in the article and implementation are anchored to publicly available breach intelligence.

## Foundation (Annual)

**Verizon 2025 Data Breach Investigations Report (DBIR)** — Primary source for breach statistics:

- Initial access vectors: credential abuse ~25%, vulnerability exploitation ~20%
- Ransomware presence: 44% of breaches, up from 32%
- Third-party involvement: 30% (doubled from 15%)
- MFA bypass: prompt bombing in 14% of social engineering incidents, 22% of Microsoft 365 MFA bypass attacks
- Edge device exploitation: 22% of exploitation targets, 8x increase from prior year
- Remediation timelines: median 94 days for leaked secrets in GitHub, median 32 days for edge device vulnerabilities
- Ransom outcomes: median payment $115,000, 64% of victims did not pay
- Edge device patching: only 54% of vulnerabilities fully remediated

## Acceleration (Q4 2025 - February 2026)

**CyberMaxx Q4 2025 Ransomware Research Report (Feb 2026):** 2,406 attacks in Q4 2025 (57% QoQ increase), 7,884 total for 2025, Akira (14%) and Qilin (13%) leading

**Cyble Ransomware Analysis (Feb 2026):** 679 attacks in January 2026, 30% above 9-month average

**Coveware Q4 2025 Ransomware Report (Feb 2026):** Median company size 200 employees (down 45% from Q3), encryption-focused attacks winning over exfiltration

**Flare 2026 State of Enterprise Infostealer Exposure (Feb 2026):** 1 in 5 infections yield enterprise access in 2026, 16% of infections expose corporate SSO (up from 6%), Microsoft Entra ID in 79% of compromised logs

**Constella 2026 Identity Breach Report (Feb 2026):** 51.7M infostealer packages processed (+72% YoY), 24.8M unique infected devices, Public/Education sectors +569% breach volume

**Microsoft Threat Intelligence (Feb 2026):** ClickFix social engineering technique, macOS infostealers via Python and malvertising

**Red Canary 2026 Threat Detection Report:** RMM tool abuse (ScreenConnect, AnyDesk, TeamViewer) as post-exploitation stealth technique

## Operational Benchmarks

- **CISA Known Exploited Vulnerabilities (KEV) Catalog & BOD 22-01:** 15-day remediation for critical KEVs on internet-facing systems
- **FBI Internet Crime Complaint Center (IC3) 2024 Report:** Business email compromise losses ($2.77 billion across 21,442 incidents)
- **MITRE ATT&CK Framework:** Kill-chain sequence modeling for defensive breakpoint analysis

## Likelihood Ratio Rationale

Likelihood ratios in the IFA examples are conservative estimates derived from:

- **KEV exposure (LR 1.8):** DBIR shows 20% exploitation vector, 22% targeting edge devices; CISA KEVs are high-confidence predictors of active exploitation
- **Infostealer exposure (LR 1.6):** 2026 estimates of 1 in 5 infections yielding enterprise access; Flare and Constella data on credential exposure
- **Third-party / RMM (LR 1.4):** DBIR third-party involvement doubled to 30%; Red Canary RMM abuse as post-exploitation vector
- **Phishing-resistant MFA (LR 0.65):** DBIR credential abuse ~25%; FIDO2/WebAuthn significantly reduces credential-based success
- **Segmentation (LR 0.70-0.75):** Limits lateral movement per ATT&CK; contains intrusions to initial segment
- **Quarterly recovery tested (LR 0.80):** DBIR 64% non-payment rate for prepared orgs; tested recovery correlates with better outcomes
- **KEV remediation SLA (LR 0.85):** CISA BOD 22-01 model; closes window vs. 32-day median edge patching
- **Automated secret detection (LR 0.90):** Reduces 94-day median exposure for leaked credentials

LRs should be updated as new breach data becomes available. The key is explicit documentation and conservatism.

## About This Model

The Impact-First Security Model (IFSM) and Impact Forecast Algorithm (IFA) are original frameworks developed for operational security teams. They synthesize public breach data into actionable architecture, not vendor recommendations. All code is provided under MIT license; modify, extend, and improve.
