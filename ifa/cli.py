"""
Minimal CLI for running IFA from the terminal.

Usage:
    ifa --prior 0.25 --factor kev:1.8:Known exploited vulns --factor mfa:0.65:FIDO2 deployed
"""

import argparse
import sys
from typing import Dict

from .core import Evidence, impact_forecast


def _parse_factor(s: str) -> tuple:
    """
    Parse a factor string of form name:lr:note.

    Raises:
        ValueError: If format is invalid or lr is not a positive float.
    """
    parts = s.split(":", 2)
    if len(parts) < 3:
        raise ValueError(
            f"Factor must be name:lr:note (e.g. kev:1.8:Known exploited vulns), got: {s}"
        )
    name, lr_str, note = parts
    name = name.strip()
    note = note.strip()
    if not name:
        raise ValueError("Factor name cannot be empty")
    try:
        lr = float(lr_str.strip())
    except ValueError:
        raise ValueError(f"Likelihood ratio must be a number, got: {lr_str}")
    if lr <= 0:
        raise ValueError(f"Likelihood ratio must be > 0, got: {lr}")
    return (name, Evidence(lr=lr, note=note))


def main() -> int:
    """Entry point for ifa CLI."""
    parser = argparse.ArgumentParser(
        description="Impact Forecast Algorithm (IFA) - Bayesian-inspired risk quantification"
    )
    parser.add_argument(
        "--prior",
        type=float,
        required=True,
        help="Prior probability (0 < p < 1)",
    )
    parser.add_argument(
        "--factor",
        action="append",
        dest="factors",
        default=[],
        metavar="NAME:LR:NOTE",
        help="Evidence factor (e.g. kev:1.8:Known exploited vulns). Repeat for multiple factors.",
    )

    args = parser.parse_args()

    if not (0 < args.prior < 1):
        print("Error: prior must be between 0 and 1 (exclusive)", file=sys.stderr)
        return 1

    if not args.factors:
        print("Error: at least one --factor is required", file=sys.stderr)
        return 1

    evidence: Dict[str, Evidence] = {}
    for raw in args.factors:
        try:
            name, ev = _parse_factor(raw)
            evidence[name] = ev
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    try:
        results = impact_forecast(prior_p=args.prior, evidence=evidence)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(f"Prior probability:    {results['prior_probability']:.1%}")
    print(f"Posterior probability: {results['posterior_probability']:.1%}")
    print(f"Risk level:          {results['risk_level']}")

    factors = results["factors"]
    by_distance = sorted(
        factors,
        key=lambda f: abs(f["lr"] - 1.0),
        reverse=True,
    )
    top3 = by_distance[:3]
    if top3:
        print("\nTop 3 factors by LR distance from 1.0:")
        for f in top3:
            direction = "risk" if f["lr"] > 1 else "protective"
            print(f"  {f['name']:30s} LR={f['lr']:.2f} ({direction})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
