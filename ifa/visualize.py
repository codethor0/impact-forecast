"""
Visualization helpers for IFA results.

Generates waterfall-style charts and risk thermometer using matplotlib.
"""

from typing import Optional

import matplotlib.pyplot as plt

from .core import odds_to_prob


def visualize_forecast(
    results: dict,
    save_path: Optional[str] = None,
):
    """
    Generate visualization of IFA results.

    Creates a two-panel figure: factor-by-factor waterfall chart and
    risk thermometer with summary.

    Args:
        results: Output from impact_forecast (must contain prior_probability,
                prior_odds, posterior_probability, absolute_change, factors,
                risk_level).
        save_path: Optional path to save figure. If None, only plt.show() is
                   called.

    Returns:
        matplotlib Figure instance.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    factors = results["factors"]
    names = ["Prior"] + [f["name"] for f in factors]
    probs = [results["prior_probability"]]
    current_odds = results["prior_odds"]

    for f in factors:
        current_odds *= f["lr"]
        probs.append(odds_to_prob(current_odds))

    colors = ["#3498db"] + [
        "#e74c3c" if f["lr"] > 1 else "#27ae60" for f in factors
    ]

    bars = ax1.barh(names, probs, color=colors, edgecolor="black", linewidth=0.5)
    ax1.set_xlim(0, max(probs) * 1.2)
    ax1.set_xlabel("Probability of Material Impact", fontsize=11)
    ax1.set_title("IFA: Factor-by-Factor Impact", fontsize=13, fontweight="bold")

    for bar, prob in zip(bars, probs):
        ax1.text(
            prob + 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{prob:.1%}",
            va="center",
            fontsize=9,
        )

    ax1.axvline(
        x=results["prior_probability"],
        color="gray",
        linestyle="--",
        alpha=0.7,
        label=f"Prior: {results['prior_probability']:.1%}",
    )
    ax1.axvline(
        x=results["posterior_probability"],
        color="red",
        linestyle="--",
        alpha=0.7,
        label=f"Posterior: {results['posterior_probability']:.1%}",
    )
    ax1.legend(loc="lower right")

    risk_colors = {
        "LOW": "#27ae60",
        "MODERATE": "#f1c40f",
        "ELEVATED": "#e67e22",
        "HIGH": "#c0392b",
    }
    risk_color = risk_colors[results["risk_level"]]

    ax2.barh(
        ["Current Risk"],
        [results["posterior_probability"]],
        color=risk_color,
        height=0.4,
        edgecolor="black",
    )
    ax2.set_xlim(0, 1)
    ax2.set_xlabel("Probability", fontsize=11)
    ax2.set_title(
        f"Risk Assessment: {results['risk_level']}",
        fontsize=13,
        fontweight="bold",
    )

    ax2.axvspan(0, 0.10, alpha=0.1, color="green", label="Low <10%")
    ax2.axvspan(0.10, 0.20, alpha=0.1, color="yellow", label="Moderate 10-20%")
    ax2.axvspan(0.20, 0.35, alpha=0.1, color="orange", label="Elevated 20-35%")
    ax2.axvspan(0.35, 1.0, alpha=0.1, color="red", label="High >35%")
    ax2.legend(loc="upper right", fontsize=9)

    summary_text = (
        f"Prior: {results['prior_probability']:.1%}\n"
        f"Posterior: {results['posterior_probability']:.1%}\n"
        f"Change: {results['absolute_change']:+.1%}\n"
        f"Factors: {len(factors)}"
    )
    ax2.text(
        0.98,
        0.02,
        summary_text,
        transform=ax2.transAxes,
        fontsize=10,
        verticalalignment="bottom",
        horizontalalignment="right",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
    )

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")

    # Avoid non-interactive backend warnings while preserving interactive behavior.
    backend = plt.get_backend().lower()
    if "agg" not in backend:
        plt.show()
    return fig
