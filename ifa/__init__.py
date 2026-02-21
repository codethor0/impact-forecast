"""
Impact Forecast Algorithm (IFA).

Bayesian-inspired risk quantification for operational security teams.
"""

from .core import Evidence, impact_forecast
from .visualize import visualize_forecast

__all__ = ["Evidence", "impact_forecast", "visualize_forecast"]
