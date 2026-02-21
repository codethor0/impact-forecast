"""
Minimal IFA example with mixed risk and protective factors.
"""

from ifa import Evidence, impact_forecast

prior = 0.20

evidence = {
    "kev_exposed": Evidence(
        lr=1.8,
        note="Known exploited vulns on edge devices",
    ),
    "flat_network": Evidence(
        lr=1.5,
        note="Lack of segmentation enables lateral movement",
    ),
    "phishing_resistant_mfa": Evidence(
        lr=0.65,
        note="FIDO2/WebAuthn for admins",
    ),
    "tested_backup_recovery": Evidence(
        lr=0.75,
        note="Quarterly tested backup/recovery",
    ),
}

results = impact_forecast(prior_p=prior, evidence=evidence)

print("=" * 60)
print("IFA BASIC EXAMPLE")
print("=" * 60)
print(f"Prior probability:     {results['prior_probability']:.1%}")
print(f"Posterior probability: {results['posterior_probability']:.1%}")
print(f"Absolute change:       {results['absolute_change']:+.1%}")
print(f"Risk level:            {results['risk_level']}")
print("-" * 60)
print("Factor log:")
for f in results["factors"]:
    direction = "risk" if f["lr"] > 1 else "protective"
    print(f"  {f['name']:25s} LR={f['lr']:.2f} ({direction})")
print("=" * 60)
