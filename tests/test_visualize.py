"""Smoke tests for visualization helpers."""

import matplotlib
matplotlib.use("Agg")

import pytest

from ifa.core import Evidence, impact_forecast
from ifa.visualize import visualize_forecast


@pytest.fixture
def sample_results():
    """Minimal valid IFA results."""
    evidence = {
        "kev": Evidence(1.8, note="KEV exposed"),
        "mfa": Evidence(0.65, note="Phishing-resistant MFA"),
    }
    return impact_forecast(prior_p=0.25, evidence=evidence)


def test_visualize_forecast_returns_fig(sample_results):
    """visualize_forecast should return a Figure without raising."""
    fig = visualize_forecast(sample_results)
    assert fig is not None
    assert hasattr(fig, "savefig")


def test_visualize_forecast_save_path(tmp_path, sample_results):
    """visualize_forecast with save_path should write file."""
    save_path = tmp_path / "test_ifa.png"
    fig = visualize_forecast(sample_results, save_path=str(save_path))
    assert save_path.exists()
    assert save_path.stat().st_size > 0


def test_visualize_forecast_empty_factors(tmp_path):
    """visualize_forecast with empty factors (LR=1 only) should not crash."""
    evidence = {"neutral": Evidence(1.0, note="No effect")}
    results = impact_forecast(prior_p=0.25, evidence=evidence)
    fig = visualize_forecast(results, save_path=str(tmp_path / "empty.png"))
    assert fig is not None
