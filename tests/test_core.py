"""Unit tests for IFA core logic."""

import pytest

from ifa.core import (
    Evidence,
    impact_forecast,
    odds_to_prob,
    prob_to_odds,
)


class TestProbOddsConversion:
    """Tests for prob_to_odds and odds_to_prob."""

    def test_inverse_functions(self):
        """prob_to_odds and odds_to_prob should be inverse."""
        for p in [0.1, 0.25, 0.5, 0.75, 0.9]:
            assert odds_to_prob(prob_to_odds(p)) == pytest.approx(p)
        for o in [0.1, 0.5, 1.0, 2.0, 9.0]:
            assert prob_to_odds(odds_to_prob(o)) == pytest.approx(o)

    def test_prob_to_odds_rejects_zero(self):
        with pytest.raises(ValueError, match="p must be between 0 and 1"):
            prob_to_odds(0)

    def test_prob_to_odds_rejects_one(self):
        with pytest.raises(ValueError, match="p must be between 0 and 1"):
            prob_to_odds(1)

    def test_prob_to_odds_rejects_negative(self):
        with pytest.raises(ValueError, match="p must be between 0 and 1"):
            prob_to_odds(-0.1)

    def test_prob_to_odds_rejects_above_one(self):
        with pytest.raises(ValueError, match="p must be between 0 and 1"):
            prob_to_odds(1.1)

    def test_odds_to_prob_rejects_zero(self):
        with pytest.raises(ValueError, match="odds must be > 0"):
            odds_to_prob(0)

    def test_odds_to_prob_rejects_negative(self):
        with pytest.raises(ValueError, match="odds must be > 0"):
            odds_to_prob(-1)


class TestImpactForecast:
    """Tests for impact_forecast."""

    def test_lr_one_leaves_prior_unchanged(self):
        """LR=1 evidence should not change posterior."""
        evidence = {
            "neutral": Evidence(lr=1.0, note="No effect"),
        }
        results = impact_forecast(prior_p=0.25, evidence=evidence)
        assert results["posterior_probability"] == pytest.approx(0.25)
        assert results["absolute_change"] == pytest.approx(0)

    def test_doubling_odds(self):
        """LR=2 doubles odds; verify manual calculation."""
        evidence = {"double": Evidence(lr=2.0, note="Doubles odds")}
        results = impact_forecast(prior_p=0.25, evidence=evidence)
        # prior odds = 0.25/0.75 = 1/3; posterior odds = 2/3
        # posterior prob = (2/3) / (1 + 2/3) = 2/5 = 0.4
        assert results["posterior_probability"] == pytest.approx(0.4)

    def test_halving_odds(self):
        """LR=0.5 halves odds."""
        evidence = {"half": Evidence(lr=0.5, note="Halves odds")}
        results = impact_forecast(prior_p=0.5, evidence=evidence)
        # prior odds = 1; posterior odds = 0.5; posterior prob = 1/3
        assert results["posterior_probability"] == pytest.approx(1 / 3)

    def test_risk_level_thresholds(self):
        """LOW < 10%, MODERATE < 20%, ELEVATED < 35%, else HIGH."""
        neutral = {"x": Evidence(1.0, "n")}
        assert impact_forecast(0.05, neutral)["risk_level"] == "LOW"
        assert impact_forecast(0.09, neutral)["risk_level"] == "LOW"
        assert impact_forecast(0.10, neutral)["risk_level"] == "MODERATE"
        assert impact_forecast(0.15, neutral)["risk_level"] == "MODERATE"
        assert impact_forecast(0.19, neutral)["risk_level"] == "MODERATE"
        assert impact_forecast(0.20, neutral)["risk_level"] == "ELEVATED"
        assert impact_forecast(0.25, neutral)["risk_level"] == "ELEVATED"
        assert impact_forecast(0.34, neutral)["risk_level"] == "ELEVATED"
        assert impact_forecast(0.35, neutral)["risk_level"] == "HIGH"
        assert impact_forecast(0.50, neutral)["risk_level"] == "HIGH"

    def test_lr_zero_raises(self):
        with pytest.raises(ValueError, match="Likelihood ratios must be > 0"):
            impact_forecast(0.25, {"x": Evidence(lr=0, note="zero")})

    def test_lr_negative_raises(self):
        with pytest.raises(ValueError, match="Likelihood ratios must be > 0"):
            impact_forecast(0.25, {"x": Evidence(lr=-1, note="negative")})

    def test_prior_zero_raises(self):
        with pytest.raises(ValueError, match="prior_p must be between"):
            impact_forecast(0, {"x": Evidence(1.0, "n")})

    def test_prior_one_raises(self):
        with pytest.raises(ValueError, match="prior_p must be between"):
            impact_forecast(1.0, {"x": Evidence(1.0, "n")})

    def test_risk_and_protective_cancel(self):
        """LR=2 and LR=0.5 should net to 1, posterior = prior."""
        evidence = {
            "risk": Evidence(2.0, note="Doubles odds"),
            "protect": Evidence(0.5, note="Halves odds"),
        }
        results = impact_forecast(prior_p=0.25, evidence=evidence)
        assert results["posterior_probability"] == pytest.approx(0.25)
        assert results["cumulative_lr"] == pytest.approx(1.0)

    def test_factor_log_preserves_order(self):
        """Factor log should reflect insertion order."""
        evidence = {
            "a": Evidence(1.5, note="A"),
            "b": Evidence(0.8, note="B"),
        }
        results = impact_forecast(prior_p=0.25, evidence=evidence)
        assert [f["name"] for f in results["factors"]] == ["a", "b"]
        assert results["factors"][0]["lr"] == 1.5
        assert results["factors"][1]["lr"] == 0.8
