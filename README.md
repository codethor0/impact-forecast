# Impact Forecast Algorithm (IFA)

[![CI](https://github.com/codethor0/impact-forecast/actions/workflows/ci.yaml/badge.svg)](https://github.com/codethor0/impact-forecast/actions/workflows/ci.yaml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/codethor0/impact-forecast/releases)

Bayesian-inspired risk quantification for operational security teams. Part of the Impact-First Security Model (IFSM).

**Author:** Thor Thor ([@codethor0](https://github.com/codethor0))  
**Article:** [One Algorithm to Kill Security Theater: The Impact-First Model for 2026](docs/impact-first-security-model-2026.md)

## Quick Start

```python
from ifa import Evidence, impact_forecast

evidence = {
    "kev_exposed": Evidence(lr=1.8, note="Known exploited vulns on edge devices"),
    "phishing_resistant_mfa": Evidence(lr=0.65, note="FIDO2/WebAuthn for admins"),
}

results = impact_forecast(prior_p=0.25, evidence=evidence)
print(results["risk_level"])
print(f"{results['posterior_probability']:.1%}")
```

## Installation

```bash
git clone https://github.com/codethor0/impact-forecast.git
cd impact-forecast
pip install -e .
```

For development with tests:

```bash
pip install -e ".[dev]"
pytest
```

Run examples (after install):

```bash
python examples/ifa_example_basic.py
python examples/ifa_example_2026_profile.py
```

## CLI

```bash
ifa --prior 0.25 --factor "kev_exposed:1.8:Known exploited vulns on edge devices" --factor "phishing_resistant_mfa:0.65:FIDO2/WebAuthn for admins"
```

## Algorithm (IFA) Summary

Given a prior probability p and likelihood ratios LR_i:

- odds = p / (1 - p)
- updated_odds = odds * (product of all LR_i)
- posterior = updated_odds / (1 + updated_odds)

Risk levels:

- LOW:       p < 0.10
- MODERATE:  0.10 <= p < 0.20
- ELEVATED:  0.20 <= p < 0.35
- HIGH:      p >= 0.35

## Documentation

- **Full Article:** [docs/impact-first-security-model-2026.md](docs/impact-first-security-model-2026.md) — IFSM theory, four impact levers, and 90-day rollout
- **Data Sources & Methodology:** [docs/methodology-and-sources.md](docs/methodology-and-sources.md) — Primary sources and likelihood ratio rationale

## Examples

- [examples/ifa_example_basic.py](examples/ifa_example_basic.py) — Minimal example with 4 factors
- [examples/ifa_example_2026_profile.py](examples/ifa_example_2026_profile.py) — February 2026 profile (15 factors)

## Visualization

```python
from ifa import Evidence, impact_forecast, visualize_forecast

results = impact_forecast(prior_p=0.25, evidence=evidence)
visualize_forecast(results, save_path="ifa_forecast.png")
```

## License

MIT License. See [LICENSE](LICENSE).
