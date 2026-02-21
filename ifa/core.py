"""
Impact Forecast Algorithm (IFA) core logic.

Bayesian-inspired risk quantification for operational security teams.
Calculates material impact probability from evidence-based likelihood ratios.
"""

from dataclasses import dataclass
from typing import Dict, List, Any


# ============================================================================
# IMPACT FORECAST ALGORITHM (IFA)
# Version: 1.0.0
# Author: Thor Thor (@codethor0)
# Repository: https://github.com/codethor0/impact-forecast
# License: MIT
#
# Description: Bayesian-inspired risk quantification for operational security
# teams. Calculates material impact probability from evidence-based likelihood
# ratios derived from open-source threat intelligence.
#
# Requirements: Python 3.8+, matplotlib, numpy
# ============================================================================

__author__ = "Thor Thor"
__version__ = "1.0.0"
__license__ = "MIT"
__url__ = "https://github.com/codethor0/impact-forecast"


@dataclass(frozen=True)
class Evidence:
    """
    A single evidence factor with a likelihood ratio and note.

    LR > 1 increases risk, LR < 1 decreases risk, LR = 1 has no effect.
    """

    lr: float
    note: str


def prob_to_odds(p: float) -> float:
    """
    Convert probability to odds.

    Args:
        p: Probability in (0, 1), exclusive.

    Returns:
        Odds = p / (1 - p).

    Raises:
        ValueError: If p is not in (0, 1).
    """
    if not (0 < p < 1):
        raise ValueError("p must be between 0 and 1 (exclusive)")
    return p / (1 - p)


def odds_to_prob(o: float) -> float:
    """
    Convert odds back to probability.

    Args:
        o: Positive odds.

    Returns:
        Probability = o / (1 + o).

    Raises:
        ValueError: If o <= 0.
    """
    if o <= 0:
        raise ValueError("odds must be > 0")
    return o / (1 + o)


def impact_forecast(prior_p: float, evidence: Dict[str, Evidence]) -> Dict[str, Any]:
    """
    Impact Forecast Algorithm (IFA).

    Updates prior probability using evidence-based likelihood ratios.
    Returns posterior probability and full analysis.

    Args:
        prior_p: Prior probability of material impact in (0, 1).
        evidence: Mapping of factor name to Evidence (lr, note).
                  Order is preserved for factor log; dicts maintain insertion order.

    Returns:
        Dict with keys: prior_probability, prior_odds, cumulative_lr,
        posterior_probability, absolute_change, relative_change,
        factors (list of factor logs), risk_level (LOW/MODERATE/ELEVATED/HIGH).

    Raises:
        ValueError: If prior_p not in (0, 1) or any LR <= 0.
    """
    if not (0 < prior_p < 1):
        raise ValueError("prior_p must be between 0 and 1 (exclusive)")

    prior_odds = prob_to_odds(prior_p)
    cumulative_lr = 1.0
    factor_log: List[Dict[str, Any]] = []

    for name, ev in evidence.items():
        if ev.lr <= 0:
            raise ValueError("Likelihood ratios must be > 0")
        cumulative_lr *= ev.lr
        factor_log.append(
            {
                "name": name,
                "lr": ev.lr,
                "note": ev.note,
                "cumulative_after": cumulative_lr,
            }
        )

    posterior_odds = prior_odds * cumulative_lr
    posterior_p = odds_to_prob(posterior_odds)

    absolute_change = posterior_p - prior_p
    relative_change = absolute_change / prior_p if prior_p > 0 else 0.0

    if posterior_p < 0.10:
        risk_level = "LOW"
    elif posterior_p < 0.20:
        risk_level = "MODERATE"
    elif posterior_p < 0.35:
        risk_level = "ELEVATED"
    else:
        risk_level = "HIGH"

    return {
        "prior_probability": prior_p,
        "prior_odds": prior_odds,
        "cumulative_lr": cumulative_lr,
        "posterior_probability": posterior_p,
        "absolute_change": absolute_change,
        "relative_change": relative_change,
        "factors": factor_log,
        "risk_level": risk_level,
    }
