import pytest

from finance_analyst.metrics import (
    MetricError, cac, ltv, ltv_cac_ratio, payback_months, pct_change,
)


def test_cac_q1_example():
    assert cac(50_000, 1_000) == 50.0


def test_ltv_q1_example():
    assert ltv(50, 24) == 1_200.0


def test_ltv_with_gross_margin():
    assert ltv(50, 24, gross_margin=0.5) == 600.0


def test_ltv_cac_ratio_q1():
    assert ltv_cac_ratio(1_200, 50) == 24.0


def test_q2_values_by_hand():
    # Q2: spend 75,000 / 1,200 customers = 62.5 ; LTV = 55 * 22 = 1,210
    assert cac(75_000, 1_200) == 62.5
    assert ltv(55, 22) == 1_210.0
    assert ltv_cac_ratio(1_210, 62.5) == pytest.approx(19.36)


def test_payback_months():
    assert payback_months(50, 50) == 1.0
    assert payback_months(60, 30, gross_margin=0.5) == 4.0


def test_pct_change():
    assert pct_change(50, 62.5) == pytest.approx(0.25)
    assert pct_change(100, 80) == pytest.approx(-0.2)


def test_cac_zero_customers_raises():
    with pytest.raises(MetricError):
        cac(110_000, 0)


def test_cac_missing_spend_raises():
    with pytest.raises(MetricError):
        cac(None, 1_000)


def test_cac_negative_spend_raises():
    with pytest.raises(MetricError):
        cac(-1, 100)


def test_cac_zero_spend_is_allowed():
    assert cac(0, 100) == 0.0


def test_ltv_zero_lifespan_raises():
    with pytest.raises(MetricError):
        ltv(50, 0)


def test_ltv_bad_margin_raises():
    with pytest.raises(MetricError):
        ltv(50, 24, gross_margin=1.5)
    with pytest.raises(MetricError):
        ltv(50, 24, gross_margin=0)


def test_ratio_zero_cac_raises():
    with pytest.raises(MetricError):
        ltv_cac_ratio(1_000, 0)


def test_pct_change_zero_baseline_raises():
    with pytest.raises(MetricError):
        pct_change(0, 10)
