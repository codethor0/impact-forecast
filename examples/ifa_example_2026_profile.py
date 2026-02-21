"""
February 2026 profile: worked example matching article evidence factors.

Prior 0.25, evidence for KEV exposure, infostealer, RMM, phishing-resistant MFA,
and other 2026 threat factors from DBIR 2025 and Feb 2026 threat intelligence.
"""

from ifa import Evidence, impact_forecast

prior = 0.25

evidence = {
    # Risk factors (LR > 1.0)
    "kev_exposed_on_edge_devices": Evidence(
        1.8,
        "Known exploited vulns present; DBIR 2025 shows 20% exploitation vector, "
        "22% targeting edge devices, 32-day median patch time",
    ),
    "unmonitored_third_party_access": Evidence(
        1.4,
        "Third-party involvement doubled to 30% of breaches; partner pathways increase exposure",
    ),
    "infostealer_enterprise_exposure": Evidence(
        1.6,
        "2026: 1 in 5 infostealer infections yields enterprise access; "
        "16% expose corporate SSO (up from 6%)",
    ),
    "mfa_fatigue_vulnerable": Evidence(
        1.2,
        "Prompt bombing in 14% of social engineering incidents, 22% of M365 MFA bypass; "
        "session hijacking rising",
    ),
    "flat_network_topology": Evidence(
        1.5,
        "Lack of segmentation enables rapid lateral movement; RMM tools increasingly weaponized",
    ),
    "untested_recovery_procedures": Evidence(
        1.3,
        "DBIR 2025: organizations without tested recovery more likely to pay; "
        "64% non-payment for prepared orgs",
    ),
    "clickfix_vulnerable": Evidence(
        1.25,
        "2026 emerging threat: ClickFix social engineering bypasses traditional controls; "
        "Microsoft identified Feb 2026",
    ),
    # Protective factors (LR < 1.0)
    "phishing_resistant_mfa_deployed": Evidence(
        0.65,
        "Reduces credential abuse vector; DBIR 2025 shows ~25% credential abuse, "
        "phishing-resistant MFA reduces success",
    ),
    "zero_standing_privilege_enforced": Evidence(
        0.70,
        "Eliminates persistent credential theft opportunities; limits blast radius including session hijacking",
    ),
    "network_segmentation_validated": Evidence(
        0.75,
        "Blocks lateral movement; contains intrusions to initial access segment; limits RMM tool abuse",
    ),
    "quarterly_recovery_tested": Evidence(
        0.80,
        "DBIR 2025: tested recovery correlates with 64% non-payment rate; "
        "essential for encryption-focused ransomware",
    ),
    "kev_remediation_15_day_sla": Evidence(
        0.85,
        "CISA BOD 22-01 model; closes window faster than 32-day median edge device patching",
    ),
    "automated_secret_detection": Evidence(
        0.90,
        "Reduces 94-day median exposure time for leaked credentials; shrinks attacker window",
    ),
    "rmm_monitoring_deployed": Evidence(
        0.88,
        "2026: Monitoring and alerting on RMM tool usage blocks post-exploitation sequences",
    ),
    "infostealer_log_monitoring": Evidence(
        0.82,
        "2026: Proactive monitoring for corporate credentials in infostealer logs; "
        "51.7M packages processed in 2025 (+72%)",
    ),
}

results = impact_forecast(prior_p=prior, evidence=evidence)

print("=" * 70)
print("IMPACT FORECAST ALGORITHM (IFA) RESULTS - FEBRUARY 2026")
print("=" * 70)
print(f"Prior Probability:        {results['prior_probability']:.1%}")
print(f"Posterior Probability:    {results['posterior_probability']:.1%}")
print(f"Absolute Change:          {results['absolute_change']:+.1%}")
print(f"Relative Change:          {results['relative_change']:+.1%}")
print(f"Risk Level:               {results['risk_level']}")
print(f"Cumulative LR:            {results['cumulative_lr']:.2f}")
print("-" * 70)

print("\nFACTOR BREAKDOWN:")
for f in results["factors"]:
    direction = "risk" if f["lr"] > 1 else "protective"
    print(f"  {f['name']:35s} LR={f['lr']:.2f} ({direction})")

risk_factors = [f for f in results["factors"] if f["lr"] > 1]
protective_factors = [f for f in results["factors"] if f["lr"] < 1]

print("\n" + "=" * 70)
print("SENSITIVITY ANALYSIS - TOP PRIORITIES FOR 2026")
print("=" * 70)
if risk_factors:
    top_risk = max(risk_factors, key=lambda x: x["lr"])
    print(f"Highest impact risk factor: {top_risk['name']}")
    print(f"  LR={top_risk['lr']:.2f} - Remediating this alone reduces probability significantly")
    reduced_evidence = {k: v for k, v in evidence.items() if k != top_risk["name"]}
    reduced_results = impact_forecast(prior, reduced_evidence)
    improvement = results["posterior_probability"] - reduced_results["posterior_probability"]
    print(f"  Estimated improvement: {improvement:.1%} reduction")

if protective_factors:
    top_protect = min(protective_factors, key=lambda x: x["lr"])
    print(f"\nStrongest protective factor: {top_protect['name']}")
    print(f"  LR={top_protect['lr']:.2f} - Maximum risk reduction when in place")

print("=" * 70)
