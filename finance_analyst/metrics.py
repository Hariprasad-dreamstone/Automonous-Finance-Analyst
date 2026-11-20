"""Deterministic unit-economics metrics.

Every number the assistant reports comes from these functions, never from
the LLM. Each function raises MetricError when the inputs cannot produce a
trustworthy answer, so the caller can refuse instead of guessing.
"""


class MetricError(ValueError):
    """Raised when a metric cannot be computed from the given inputs."""


def _require_positive(name: str, value) -> None:
    if value is None:
        raise MetricError(f"{name} is missing")
    if value <= 0:
        raise MetricError(f"{name} must be greater than 0 (got {value})")


def cac(marketing_spend: float, new_customers: int) -> float:
    """Customer Acquisition Cost = marketing spend / new customers."""
    if marketing_spend is None:
        raise MetricError("marketing_spend is missing")
    if marketing_spend < 0:
        raise MetricError("marketing_spend cannot be negative")
    _require_positive("new_customers", new_customers)
    return marketing_spend / new_customers


def ltv(monthly_revenue_per_user: float, lifespan_months: float,
        gross_margin: float = 1.0) -> float:
    """Lifetime Value = monthly revenue per user x lifespan x gross margin.

    gross_margin defaults to 1.0 (revenue-based LTV), matching the original
    v1 app. Pass e.g. 0.7 for margin-based LTV.
    """
    _require_positive("monthly_revenue_per_user", monthly_revenue_per_user)
    _require_positive("lifespan_months", lifespan_months)
    if gross_margin is None or not (0 < gross_margin <= 1):
        raise MetricError("gross_margin must be between 0 (exclusive) and 1")
    return monthly_revenue_per_user * lifespan_months * gross_margin


def ltv_cac_ratio(ltv_value: float, cac_value: float) -> float:
    """LTV / CAC. Above ~3 is the usual rule of thumb for healthy economics."""
    _require_positive("cac", cac_value)
    if ltv_value is None or ltv_value < 0:
        raise MetricError("ltv must be zero or greater")
    return ltv_value / cac_value


def payback_months(cac_value: float, monthly_revenue_per_user: float,
                   gross_margin: float = 1.0) -> float:
    """Months of revenue needed to earn back the acquisition cost."""
    _require_positive("monthly_revenue_per_user", monthly_revenue_per_user)
    if cac_value is None or cac_value < 0:
        raise MetricError("cac must be zero or greater")
    if not (0 < gross_margin <= 1):
        raise MetricError("gross_margin must be between 0 (exclusive) and 1")
    return cac_value / (monthly_revenue_per_user * gross_margin)


def pct_change(old: float, new: float) -> float:
    """Percentage change from old to new (0.25 means +25%)."""
    if old is None or new is None:
        raise MetricError("both values are required")
    if old == 0:
        raise MetricError("cannot compute change from a zero baseline")
    return (new - old) / old
